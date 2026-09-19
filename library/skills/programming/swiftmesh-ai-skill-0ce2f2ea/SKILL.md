---
name: "swiftmesh-ai-skill"
description: "Comprehensive guide for using SwiftMesh, an Alamofire + Codable wrapper with async/await, Combine, fluent configuration, file upload/download, JSON key path parsing, resilient Codable wrappers, and logging."
---

# SwiftMesh AI Skill

> A comprehensive AI reference for using SwiftMesh — an Alamofire + Codable wrapper with async/await, Combine, fluent configuration, file upload/download, JSON key path parsing, resilient Codable wrappers, and built-in logging.

---

## Quick Reference Card

| Feature | Method | Description |
|---------|--------|-------------|
| **GET Request** | `.request(of: Model.self)` | Decode response to Codable model |
| **Key Path** | `.request(of: Model.self, modelKeyPath: "data.user")` | Extract nested JSON |
| **File Upload** | `.upload(of: Result.self)` | Upload file/Data/stream/multipart |
| **File Download** | `.download()` | Download or resume download |
| **Raw Data** | `.requestData()` | Get raw response Data |
| **Raw String** | `.requestString()` | Get response as String |
| **Retry Policy** | `.setInterceptor(RetryPolicy())` | Auto-retry with backoff |
| **Logging** | `Mesh.enableLog()` | Enable network logging |

---

## Core Architecture

SwiftMesh uses a **builder pattern** on the `Mesh` class. Every configuration method returns `Self`, enabling fluent chaining. The flow is:

```
Configure (Mesh + Config) → Execute (Request/Upload/Download) → Handle (Handle)
```

### File Structure

| File | Purpose |
|------|---------|
| `Mesh.swift` | Core builder class with all properties |
| `Config.swift` | Fluent chainable setters + global config |
| `Request.swift` | async/await request execution |
| `Handle.swift` | URL construction, error handling, response processing, RetryPolicy |
| `Upload.swift` | File upload (file, data, stream, multipart) |
| `Download.swift` | File download (standard, resumable) |
| `KeyPath.swift` | JSON key path decoder for nested extraction |
| `Codable+.swift` | Resilient property wrappers (@Default, @IgnoreError, @ConvertTo*) |
| `Log.swift` | Network logger (cURL, status, timing, JSON) |

---

## Usage Patterns

### 1. Basic GET Request

```swift
let result = try await Mesh()
    .setRequestMethod(.get)
    .setUrlHost("https://api.example.com")
    .setUrlPath("/weather/city/101030100")
    .request(of: Weather.self)
```

### 2. GET with JSON Key Path Extraction

```swift
let yesterday = try await Mesh()
    .setRequestMethod(.get)
    .setUrlHost("https://api.example.com")
    .setUrlPath("/weather")
    .request(of: Forecast.self, modelKeyPath: "data.yesterday")
```

### 3. POST Request with Parameters

```swift
let result = try await Mesh()
    .setRequestMethod(.post)
    .setUrlHost("https://api.example.com")
    .setUrlPath("/login")
    .setParameters(["username": "admin", "password": "123456"])
    .request(of: LoginResult.self)
```

### 4. POST with JSON Encoding

```swift
let result = try await Mesh()
    .setRequestMethod(.post)
    .setUrlHost("https://api.example.com")
    .setUrlPath("/api/data")
    .setRequestEncoding(JSONEncoding.default)
    .setParameters(["key": "value"])
    .request(of: Response.self)
```

### 5. Request with Custom Headers

```swift
let result = try await Mesh()
    .setUrlHost("https://api.example.com")
    .setUrlPath("/secure/data")
    .setHeads(["Authorization": "Bearer token123"])
    .request(of: SecureData.self)
```

### 6. Request with Retry Policy

```swift
let result = try await Mesh()
    .setUrlHost("https://api.example.com")
    .setUrlPath("/unstable-api")
    .setInterceptor(RetryPolicy(maxRetryCount: 3))
    .request(of: Data.self)
```

### 7. URLRequest‑based Request

```swift
let urlRequest = try URLRequest(url: URL(string: "https://api.example.com/data")!, method: .get)
let result = try await Mesh()
    .urlRequest(urlRequest, type: Response.self)
```

### 8. Raw Data Response

```swift
let data = try await Mesh()
    .setRequestMethod(.get)
    .setUrlHost("https://api.example.com")
    .setUrlPath("/raw")
    .requestData()
```

### 9. Raw String Response

```swift
let string = try await Mesh()
    .setRequestMethod(.get)
    .setUrlHost("https://api.example.com")
    .setUrlPath("/text")
    .requestString()
```

### 10. File Download

```swift
let fileURL = try await Mesh()
    .setRequestMethod(.get)
    .setUrlHost("https://example.com")
    .setUrlPath("/files/document.pdf")
    .setDestination { _, _ in
        let dest = FileManager.default.urls(for: .documentDirectory, in: .userDomainMask)[0]
            .appendingPathComponent("document.pdf")
        return (dest, [.removePreviousFile, .createIntermediateDirectories])
    }
    .download()
```

### 11. Resumable Download

```swift
let fileURL = try await Mesh()
    .setUrlHost("https://example.com")
    .setUrlPath("/files/large-file.zip")
    .setDownloadType(.resume)
    .setResumeData(savedResumeData)
    .download()
```

### 12. Single File Upload (URL)

```swift
let result = try await Mesh()
    .setRequestMethod(.post)
    .setUrlHost("https://api.example.com")
    .setUrlPath("/upload")
    .setUploadType(.file)
    .setFileURL(fileURL)
    .upload(of: UploadResult.self)
```

### 13. Single File Upload (Data)

```swift
let result = try await Mesh()
    .setRequestMethod(.post)
    .setUrlHost("https://api.example.com")
    .setUrlPath("/upload")
    .setUploadType(.data)
    .setFileData(imageData)
    .upload(of: UploadResult.self)
```

### 14. Multipart Form Upload

```swift
let result = try await Mesh()
    .setRequestMethod(.post)
    .setUrlHost("https://api.example.com")
    .setUrlPath("/upload/multi")
    .setUploadType(.multipart)
    .setAddformData(name: "file",
                    fileName: "photo.jpg",
                    fileData: imageData,
                    mimeType: "image/jpeg")
    .setAddformData(name: "description",
                    fileData: "My photo".data(using: .utf8))
    .upload(of: UploadResult.self)
```

### 15. Multipart with Pre‑built UploadDatas

```swift
let uploads = [
    MultipleUpload.formData(name: "file1", fileName: "a.jpg", fileData: data1, mimeType: "image/jpeg"),
    MultipleUpload.formData(name: "file2", fileName: "b.pdf", fileURL: fileURL)
]

let result = try await Mesh()
    .setRequestMethod(.post)
    .setUrlHost("https://api.example.com")
    .setUrlPath("/upload/batch")
    .setUploadType(.multipart)
    .setUploadDatas(uploads)
    .setParameters(["userId": "123"]) // additional form fields
    .upload(of: BatchResult.self)
```

### 16. Custom Timeout

```swift
let result = try await Mesh()
    .setUrlHost("https://api.example.com")
    .setUrlPath("/slow-api")
    .setTimeout(60) // 60 seconds
    .request(of: Response.self)
```

---

## Global Configuration

Set these once at app launch (e.g., in `AppDelegate`):

```swift
Mesh.enableLog(.log)  // or .print
Mesh.setHeaders(["Authorization": "Bearer token", "App-Version": "1.0"])
Mesh.setParameters(["platform": "ios", "sdk_version": "2.0"])
Mesh.setUrlHost("https://api.example.com")
```

Then per‑request configuration only needs the path:

```swift
let result = try await Mesh()
    .setUrlPath("/weather")
    .request(of: Weather.self)
```

---

## Resilient Codable Property Wrappers

Handle inconsistent API responses gracefully without decoding failures.

### @Default Wrappers

```swift
struct Response: Codable {
    @Default.True var isEnabled: Bool
    @Default.False var isDeleted: Bool
    @Default.EmptyString var name: String
    @Default.EmptyInt var count: Int
    @Default.EmptyArray var tags: [String]
    @Default.EmptyDictionary var meta: [String: Int]
    @Default.Now var createdAt: Date
}
```

### @IgnoreError

```swift
struct Response: Codable {
    @IgnoreError var description: String?
    @IgnoreError var nested: NestedModel?
}
```

### @ConvertToString, @ConvertToInt, @ConvertToDouble, @ConvertToFloat

These wrappers accept multiple JSON types and convert them to the desired Swift type. See the original document for usage examples.

---

## JSON Key Path Decoder

Extract nested JSON values without parsing the entire response:

```swift
let firstItem = try await Mesh()
    .setRequestMethod(.get)
    .setUrlPath("/items")
    .request(of: Item.self, modelKeyPath: "data.list.0")
```

The decoder also provides direct methods:

```swift
let decoder = JSONDecoder.default
let item = try decoder.decode(Item.self, from: jsonData, keyPath: "data.list.0")
let items = try decoder.decodeArray([Item].self, from: jsonData, keyPath: "data.list")
```

---

## Combine + SwiftUI Integration

### ObservableObject Pattern

```swift
class RequestModel: ObservableObject {
    @MainActor @Published var weather: Weather?
    @MainActor @Published var errorMessage: String?
    
    func fetchWeather() {
        Task {
            do {
                let result = try await Mesh()
                    .setRequestMethod(.get)
                    .setUrlHost("https://api.example.com")
                    .setUrlPath("/weather")
                    .request(of: Weather.self)
                await MainActor.run { self.weather = result }
            } catch {
                await MainActor.run { self.errorMessage = error.localizedDescription }
            }
        }
    }
}
```

### SwiftUI Usage

```swift
struct WeatherView: View {
    @StateObject private var model = RequestModel()
    var body: some View {
        VStack {
            if let weather = model.weather {
                Text("\(weather.temperature)°C")
            }
            if let error = model.errorMessage {
                Text(error).foregroundColor(.red)
            }
        }
        .onAppear { model.fetchWeather() }
    }
}
```

---

## Error Handling

SwiftMesh normalizes common network errors into user‑friendly `NSError` codes. All normalized errors return the message `"Unable to connect to the server"`. Catch errors as shown:

```swift
do {
    let result = try await Mesh()
        .setUrlPath("/api")
        .request(of: Response.self)
} catch let error as NSError {
    print("Error \(error.code): \(error.localizedDescription)")
}
```

---

## RetryPolicy

Built‑in retry with linear backoff (1s, 2s, 3s…):

```swift
let policy = RetryPolicy() // default 3 retries
let custom = RetryPolicy(maxRetryCount: 5)
let result = try await Mesh()
    .setUrlPath("/unstable-api")
    .setInterceptor(policy)
    .request(of: Response.self)
```

---

## Logging

Enable at app launch:

```swift
Mesh.enableLog(.log)   // Apple os.log
Mesh.enableLog(.print) // Swift print()
```

Logs include cURL command, status code, elapsed time, and pretty‑printed JSON.

---

## Configuration Method Reference

All configuration methods are chainable and return `Self`. See the original tables for the full list of request, download, upload, and global static methods.

---

## AI Prompt Templates

Use these templates when asking an AI coding assistant to generate SwiftMesh code:

### "Make a GET request"
```
Use SwiftMesh to make a GET request to {URL} and decode the response into a {Model} struct. Use key path "{keyPath}" to extract nested data.
```

### "Upload a file"
```
Use SwiftMesh to upload a {file/data/stream} to {URL} with multipart form field name "{name}" and MIME type "{mimeType}". Decode the response as {Model}.
```

### "Download a file"
```
Use SwiftMesh to download a file from {URL} and save it to {destination}. Use resumable download if needed.
```

### "Handle inconsistent API types"
```
Create a Codable struct for this JSON: {json}. Use @Default, @IgnoreError, and @ConvertTo* wrappers to handle missing or inconsistent types.
```
