// ContentView.swift

import SwiftUI

struct ContentView: View {
    
    @State private var lastProcessedText: String = ""
    @State private var scanTimer: Timer?
    @AppStorage("isAutoScanEnabled") private var isAutoScanEnabled: Bool = true
    
    private let mlConnector = MLConnector()
    
    // --- ADD THIS ---
    private let calendarManager = CalendarManager()
    
    var body: some View {
        VStack(spacing: 10) {
            Text("Event Sniffer")
                .font(.headline)
            
            Button("Scan Active Window Now") {
                Task {
                    await self.manualScan()
                }
            }
            
            Toggle("Auto-scan", isOn: $isAutoScanEnabled)
                .toggleStyle(.checkbox)
            
            Divider()
            
            // --- NEW BUTTON ---
            // A helper to ask for calendar permission up-front
            Button("Check Calendar Permission") {
                calendarManager.requestCalendarPermission { granted in
                    if granted {
                        print("Calendar permission is good!")
                    } else {
                        print("Calendar permission denied.")
                    }
                }
            }
            
            Button("Quit") {
                NSApplication.shared.terminate(nil)
            }
        }
        .padding(10)
        .frame(width: 250)
        .onAppear {
            if isAutoScanEnabled {
                startTimer()
            }
        }
        .onDisappear {
            stopTimer()
        }
        .onChange(of: isAutoScanEnabled) { newValue in
            if newValue {
                startTimer()
            } else {
                stopTimer()
            }
        }
    }
    
    // ... (startTimer and stopTimer are unchanged) ...
    
    func startTimer() {
        guard scanTimer == nil else { return }
        print("Starting scan timer...")
        scanTimer = Timer.scheduledTimer(withTimeInterval: 3.0, repeats: true) { _ in
            Task {
                await self.autoScan()
            }
        }
    }
    
    func stopTimer() {
        guard scanTimer != nil else { return }
        print("Stopping scan timer.")
        scanTimer?.invalidate()
        scanTimer = nil
    }

    func autoScan() async {
        guard let text = AccessibilityReader.readFocusedWindowText(), !text.isEmpty else {
            return
        }
        
        if text == lastProcessedText {
            return
        }
        
        self.lastProcessedText = text
        
        print("--- (AUTO) NEW TEXT DETECTED, SENDING TO ML... ---")
        await processText(text)
    }
    
    func manualScan() async {
        print("--- Manual Scan Triggered ---")
        
        guard let text = AccessibilityReader.readFocusedWindowText(), !text.isEmpty else {
            print("Manual Scan: No text found in active window.")
            return
        }
        
        self.lastProcessedText = text
        
        print("--- (MANUAL) NEW TEXT DETECTED, SENDING TO ML... ---")
        await processText(text)
    }
    
    // --- THIS FUNCTION IS NOW FULLY REPLACED ---
    func processText(_ text: String) async {
        
        let entities = await mlConnector.parseText(text)
        
        if entities.isEmpty {
            print("ML Model found no entities.")
            return
        }
        
        print("--- ✅ ML MODEL FOUND EVENTS! ---")
        for entity in entities {
            print("  -> \(entity.text) (\(entity.label))")
        }
        print("-----------------------------------")
        
        // --- THIS IS THE NEW PAYOFF LOGIC ---
        // Let's "parse" the entities into a simple event
        // This is a VERY simple parser, but it's a start!
        
        let eventTitle = entities.first(where: { $0.label == "EVENT" })?.text ?? "New Event"
        let eventDate = entities.first(where: { $0.label == "DATE" })?.text ?? ""
        let eventTime = entities.first(where: { $0.label == "TIME" })?.text ?? ""
        let eventLocation = entities.first(where: { $0.label == "LOCATION" })?.text ?? ""

        // We only care if we found *at least* an event or a date
        guard eventTitle != "New Event" || !eventDate.isEmpty else {
            print("Found entities, but not enough to make a calendar event.")
            return
        }

        // We have a potential event! Show the notification.
        let notificationTitle = "Found Event: \(eventTitle)"
        let notificationBody = "On: \(eventDate) at \(eventTime). Location: \(eventLocation)"
        
        // We'll pass this data to the notification
        let eventData: [String: String] = [
            "title": eventTitle,
            "dateText": eventDate, // We'll parse the date later
            "timeText": eventTime,
            "locationText": eventLocation
        ]
        
        NotificationManager.showNotification(
            title: notificationTitle,
            body: notificationBody,
            eventData: eventData
        )
    }
}
