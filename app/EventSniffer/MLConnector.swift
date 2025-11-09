// MLConnector.swift

import Foundation

// --- 1. Define the "Shape" of the JSON Response ---
// Our Python server sends: {"entities": [{"text": "...", "label": "..."}]}
// These structs must match that shape exactly.

struct ParseResponse: Decodable {
    let entities: [Entity]
}

struct Entity: Decodable, Identifiable {
    let id = UUID() // Add this for use in SwiftUI lists later
    let text: String
    let label: String
}

// --- 2. Define the "Shape" of the Request Body ---
// We need to send: {"text": "the scanned text..."}
struct ParseRequest: Encodable {
    let text: String
}


// --- 3. The Network Client ---
// This class will handle all the networking for us.

class MLConnector {
    
    // The URL for our local Python server
    private let parseURL = URL(string: "http://127.0.0.1:5000/parse")!
    
    // This is the main function we'll call from our ContentView
    // It's marked 'async' because networking takes time.
    func parseText(_ text: String) async -> [Entity] {
        
        // 1. Prepare the request
        var request = URLRequest(url: parseURL)
        request.httpMethod = "POST"
        // Tell the server we are sending JSON
        request.addValue("application/json", forHTTPHeaderField: "Content-Type")
        
        // 2. Encode our text into a JSON object
        let requestBody = ParseRequest(text: text)
        do {
            request.httpBody = try JSONEncoder().encode(requestBody)
        } catch {
            print("Error encoding request: \(error)")
            return []
        }
        
        // 3. Send the request and wait for a response
        do {
            let (data, response) = try await URLSession.shared.data(for: request)
            
            // Basic error checking
            if let httpResponse = response as? HTTPURLResponse, httpResponse.statusCode != 200 {
                print("HTTP Error: status code \(httpResponse.statusCode)")
                return []
            }
            
            // 4. Decode the JSON response
            let parseResponse = try JSONDecoder().decode(ParseResponse.self, from: data)
            return parseResponse.entities
            
        } catch {
            print("Network request failed: \(error)")
            // This error often happens if the Python server isn't running
            if (error as NSError).code == -1004 { // "Could not connect to server"
                print("---!!!---")
                print("ERROR: Cannot connect to Python server. Is 'python server.py' running?")
                print("---!!!---")
            }
            return []
        }
    }
}
