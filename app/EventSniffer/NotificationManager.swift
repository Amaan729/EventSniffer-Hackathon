// NotificationManager.swift

import Foundation
import UserNotifications

class NotificationManager {

    // We'll pass a unique ID for each event
    static let notificationCategoryID = "EVENT_SNIFFER_CATEGORY"

    // This function builds and shows the notification
    static func showNotification(title: String, body: String, eventData: [String: String]) {
        let center = UNUserNotificationCenter.current()

        let content = UNMutableNotificationContent()
        content.title = title
        content.body = body
        content.sound = .default

        // --- This is the "magic" ---
        // We're attaching the raw event data (title, date, etc.)
        // to the notification's 'userInfo' dictionary.
        // When the user clicks "Add", we'll read this data back.
        content.userInfo = eventData
        content.categoryIdentifier = notificationCategoryID // Connects to our "Add" action

        let request = UNNotificationRequest(identifier: UUID().uuidString,
                                            content: content,
                                            trigger: nil) // Show immediately

        center.add(request) { error in
            if let error = error {
                print("Error showing notification: \(error)")
            }
        }
    }
}
