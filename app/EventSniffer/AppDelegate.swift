// AppDelegate.swift

import SwiftUI
import UserNotifications
import EventKit

class AppDelegate: NSObject, NSApplicationDelegate, UNUserNotificationCenterDelegate {
    
    private let calendarManager = CalendarManager()

    func applicationDidFinishLaunching(_ notification: Notification) {
        checkAccessibilityPermission()
        requestNotificationPermission()
        
        let addAction = UNNotificationAction(identifier: "ADD_TO_CALENDAR",
                                             title: "Add to Calendar",
                                             options: .foreground)
        
        let category = UNNotificationCategory(identifier: NotificationManager.notificationCategoryID,
                                              actions: [addAction],
                                              intentIdentifiers: [],
                                              options: [])
        
        UNUserNotificationCenter.current().setNotificationCategories([category])
    }
    
    // This function is called when the user clicks a notification button
    func userNotificationCenter(_ center: UNUserNotificationCenter,
                                didReceive response: UNNotificationResponse,
                                withCompletionHandler completionHandler: @escaping () -> Void) {
        
        let userInfo = response.notification.request.content.userInfo
        
        if response.actionIdentifier == "ADD_TO_CALENDAR" {
            print("--- User Clicked 'Add to Calendar' ---")
            
            guard let title = userInfo["title"] as? String,
                  let dateText = userInfo["dateText"] as? String,
                  let timeText = userInfo["timeText"] as? String else { // Also get timeText
                print("Error: Notification was missing event data.")
                completionHandler()
                return
            }
            
            // --- THIS IS THE NEW, SMARTER PARSER ---
            
            var baseDate: Date
            
            // 1. Get the base day (today or tomorrow)
            if dateText.lowercased().contains("tomorrow") {
                baseDate = Calendar.current.date(byAdding: .day, value: 1, to: Date())!
            } else {
                baseDate = Date() // Default to today
            }
            
            // 2. Extract the hour from the timeText (e.g., "at 10am")
            var hour = 9 // Default to 9am if we fail
            
            // Find the first number in the timeText
            let numbers = timeText.components(separatedBy: CharacterSet.decimalDigits.inverted).joined()
            if let h = Int(numbers) {
                hour = h // We found "10"
            }
            
            // 3. Check for "am" or "pm"
            if timeText.lowercased().contains("pm") && hour < 12 {
                hour += 12 // e.g., "3pm" becomes 15
            }
            if timeText.lowercased().contains("am") && hour == 12 {
                 hour = 0 // "12am" (midnight) becomes 0
            }
            
            // 4. Create the final date by setting the hour
            guard let eventDate = Calendar.current.date(bySettingHour: hour, minute: 0, second: 0, of: baseDate) else {
                print("Error: Could not construct final date.")
                completionHandler()
                return
            }
            
            // We have what we need! Create the event.
            calendarManager.createEvent(title: title, date: eventDate)
        }
        
        completionHandler()
    }

    // ... (rest of the file is unchanged) ...
    
    func requestNotificationPermission() {
        let center = UNUserNotificationCenter.current()
        center.delegate = self
        
        center.requestAuthorization(options: [.alert, .sound]) { (granted, error) in
            if granted {
                print("Notification permission granted.")
            } else {
                print("Notification permission denied.")
            }
        }
    }
    
    func userNotificationCenter(_ center: UNUserNotificationCenter,
                                willPresent notification: UNNotification,
                                withCompletionHandler completionHandler: @escaping (UNNotificationPresentationOptions) -> Void) {
        completionHandler([.banner, .sound])
    }

    func checkAccessibilityPermission() {
        let options: NSDictionary = [kAXTrustedCheckOptionPrompt.takeUnretainedValue() as String: true]
        let isTrusted = AXIsProcessTrustedWithOptions(options)
        
        if isTrusted {
            print("Accessibility permission already granted.")
        } else {
            print("Requesting accessibility permission...")
        }
    }
}
