// AccessibilityReader.swift

import Foundation
import AppKit

class AccessibilityReader {
    
    // This is the public entry point.
    static func readFocusedWindowText() -> String? {
        
        guard let frontmostApp = NSWorkspace.shared.frontmostApplication else {
            print("Error: Could not find frontmost application.")
            return nil
        }
        
        let appElement = AXUIElementCreateApplication(frontmostApp.processIdentifier)
        
        // --- THIS IS THE NEW LOGIC ---
        // 1. First, try to get the *specific UI element* that has focus (e.g., the text box)
        var focusedElement: AnyObject?
        let focusedResult = AXUIElementCopyAttributeValue(appElement, kAXFocusedUIElementAttribute as CFString, &focusedElement)
        
        if focusedResult == .success, let focusedUIElement = focusedElement as! AXUIElement? {
            // 2. We found a focused element! Now just get the text from THAT element.
            if let text = getText(from: focusedUIElement) {
                // print("Surgical Read: Found focused text box.")
                return text
            }
        }
        
        // 3. FALLBACK: If we couldn't find a focused element (or it had no text),
        // go back to our old "read the whole window" method.
        // print("Surgical Read Failed: Falling back to whole window scan.")
        return readTextFromFocusedWindow(appElement: appElement)
    }
    
    // This is our NEW helper function to get text from a *single* element
    private static func getText(from element: AXUIElement) -> String? {
        var value: AnyObject?
        if AXUIElementCopyAttributeValue(element, kAXValueAttribute as CFString, &value) == .success {
            if let text = value as? String, !text.isEmpty {
                return text
            }
        }
        return nil // No text value found
    }
    
    // This is our OLD function, now renamed and used as a fallback
    private static func readTextFromFocusedWindow(appElement: AXUIElement) -> String? {
        var focusedWindow: AnyObject?
        let windowResult = AXUIElementCopyAttributeValue(appElement, kAXFocusedWindowAttribute as CFString, &focusedWindow)
        
        if windowResult != .success {
            return nil // No focused window
        }
        
        guard let focusedWindowElement = focusedWindow as! AXUIElement? else {
            return nil
        }
        
        // Start the recursive search
        let textSnippets = findTextIn(element: focusedWindowElement)
        
        if textSnippets.isEmpty {
            return nil
        }
        
        return textSnippets.joined(separator: "\n")
    }
    
    // This recursive function is unchanged
    private static func findTextIn(element: AXUIElement) -> [String] {
        var allText = [String]()
        
        var value: AnyObject?
        if AXUIElementCopyAttributeValue(element, kAXValueAttribute as CFString, &value) == .success {
            if let text = value as? String, !text.isEmpty {
                allText.append(text)
            }
        }
        
        var title: AnyObject?
        if AXUIElementCopyAttributeValue(element, kAXTitleAttribute as CFString, &title) == .success {
            if let text = title as? String, !text.isEmpty {
                allText.append(text)
            }
        }

        var children: AnyObject?
        let childrenResult = AXUIElementCopyAttributeValue(element, kAXChildrenAttribute as CFString, &children)
        
        if childrenResult == .success, let childElements = children as? [AXUIElement] {
            for child in childElements {
                allText.append(contentsOf: findTextIn(element: child))
            }
        }
        
        return allText
    }
}
