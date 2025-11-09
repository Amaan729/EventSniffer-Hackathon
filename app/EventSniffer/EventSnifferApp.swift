// EventSnifferApp.swift

import SwiftUI

@main
struct EventSnifferApp: App {
    
    @NSApplicationDelegateAdaptor(AppDelegate.self) var appDelegate
    
    var body: some Scene {
        // This is what creates the menu bar icon and its dropdown menu
        MenuBarExtra("EventSniffer", systemImage: "calendar.badge.plus") {
            // We will add our "content" view here
            // For now, it just has a Quit button.
            ContentView()
        }
    }
}
