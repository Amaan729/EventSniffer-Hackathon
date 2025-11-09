// CalendarManager.swift

import Foundation
import EventKit // Import the calendar framework

class CalendarManager {

    private let eventStore = EKEventStore()

    // 1. Request Permission
    // We have to ask for permission before we can do anything.
    func requestCalendarPermission(completion: @escaping (Bool) -> Void) {
        // Check the current status
        let status = EKEventStore.authorizationStatus(for: .event)

        switch status {
        case .authorized:
            completion(true) // Already have it

        case .notDetermined:
            // Not asked yet. Ask now.
            eventStore.requestFullAccessToEvents { (granted, error) in
                if let error = error {
                    print("Error requesting calendar access: \(error)")
                }
                completion(granted)
            }

        case .denied, .restricted:
            completion(false) // User said no

        @unknown default:
            completion(false)
        }
    }

    // 2. Create the Event
    // This function will be called AFTER the user clicks "Add"
    func createEvent(title: String, date: Date) {

        // First, make sure we have permission
        requestCalendarPermission { [weak self] granted in
            guard let self = self, granted else {
                print("Cannot create event, calendar permission denied.")
                return
            }

            let event = EKEvent(eventStore: self.eventStore)
            event.title = title
            event.startDate = date
            event.endDate = date.addingTimeInterval(3600) // Default to 1 hour
            event.calendar = self.eventStore.defaultCalendarForNewEvents

            do {
                try self.eventStore.save(event, span: .thisEvent)
                print("✅ Event saved to calendar!")
            } catch {
                print("Error saving event: \(error)")
            }
        }
    }
}
