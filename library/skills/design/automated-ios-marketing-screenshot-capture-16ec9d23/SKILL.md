---
name: "ios-marketing-capture"
description: "Automate reproducible marketing screenshot capture for a SwiftUI iOS app across locales, devices, and appearances. Generates full‑screen shots and isolated element renders (cards, widgets, charts) with deterministic naming."
---

# iOS Marketing Capture

## Overview
Automate marketing‑ready screenshots for a SwiftUI iOS app. The workflow produces two output streams:
1. **Full‑screen captures** – each marketing‑relevant screen with real status‑bar chrome.
2. **Element captures** – isolated renders of cards, widgets, charts, etc., with transparent corners.

The skill implements the **capture** step; post‑processing (device mock‑ups, gradients) can be handled by a separate `app-store-screenshots` skill.

## Core Approach
The solution runs **in‑app** (DEBUG‑only) rather than XCUITest. Benefits:
- No extra test target or pbxproj surgery.
- Faster iteration – just relaunch the binary.
- Direct access to ViewModels, SwiftData, `ImageRenderer`, and `UIWindow.drawHierarchy`.
- Required for rendering widgets and isolated components.

### How It Works
1. Add a `MarketingCapture.swift` file (DEBUG‑only) to the main app target.
2. Launch the app with `-MarketingCapture 1`. The file seeds demo data, then a coordinator walks a list of `CaptureStep`s – each step navigates, waits, snapshots, and cleans up.
3. PNGs are written to `Documents/marketing/<locale>/` inside the app sandbox.
4. A shell script builds the app, installs it, and loops over locales using `simctl launch` with `-AppleLanguages` / `-AppleLocale`. Files are extracted via `simctl get_app_container`.

## Process
### Step 1 – Gather Requirements
Ask the user (one question at a time) for:
1. Screens to capture (navigation paths).
2. Isolated elements (cards, widgets, charts, etc.).
3. Locales (all, subset, or explicit list).
4. Simulator device (e.g., iPhone 17 6.1" for iOS 26).
5. Appearance (light, dark, both).
6. Demo‑data strategy (auto‑seed, debug button, manual, or none).

### Step 2 – Exploration
Inspect the codebase to determine:
- Project group type (synchronized folder groups).
- Root navigation pattern (`TabView`, `NavigationStack`, `NavigationSplitView`, or custom).
- Deep‑link handling.
- Location of demo‑data seeders.
- Widget target membership.
- Presence of Live Activities or CloudKit‑backed SwiftData.
- Views that need a non‑default state for capture.

### Step 3 – Present Design
Summarize the plan and obtain explicit approval before writing code. Include:
1. Architecture overview.
2. File list to be created/modified.
3. Per‑screen navigation plan.
4. Capture ordering rationale.
5. Element‑rendering approach.
6. Output folder layout and naming.
7. Known gotchas for the project.
8. Any required primed view state.

### Step 4 – Implement
Use the templates in `templates/` as reference (not copy‑paste). Create:
- `MarketingCapture.swift` – launch‑arg parsing, snapshot helpers, `CaptureStep` definition, coordinator, element harness.
- Hook in the root view (e.g., `ContentView.swift`) to seed data and start the coordinator when the launch flag is present.
- DEBUG‑gated view modifications for primed state.
- `scripts/capture-marketing.sh` – build, install, locale loop, extraction.
- Add `marketing/` to `.gitignore`.

#### Example `CaptureStep`
```swift
struct CaptureStep {
    let name: String                     // output filename, e.g. "01-home"
    let navigate: @MainActor () -> Void   // put app in correct state
    let settle: Duration                 // wait for animations / loads
    let cleanup: (@MainActor () -> Void)? // optional teardown
}
```
Coordinator loop (simplified):
```swift
for step in steps {
    step.navigate()
    try? await Task.sleep(for: step.settle)
    if let image = MarketingCapture.snapshotKeyWindow() {
        MarketingCapture.writePNG(image, name: step.name)
    }
    step.cleanup?()
    try? await Task.sleep(for: .milliseconds(400))
}
```

#### Navigation Patterns
- **TabView** – switch `selectedTab` index.
- **NavigationStack** – push/pop routes via a router.
- **NavigationSplitView** – set sidebar and detail selections.

#### Priming View State
Add static vars in `MarketingCapture` (e.g., `pendingElapsedSeconds`) and read them in a DEBUG‑gated `.onAppear` in the target view. The coordinator sets these vars before navigation and clears them afterward.

#### Demo Data Seeder
If none exists, create `DemoDataSeeder.swift` (DEBUG only) that inserts realistic items into `ModelContext`. Make it idempotent.

#### Element Rendering
Use `ImageRenderer` at 3× scale with transparent corners. Example for a card:
```swift
let card = ItemCard(item: item, theme: theme)
    .frame(width: 380)
    .background(theme.background)
    .clipShape(RoundedRectangle(cornerRadius: 20))
let renderer = ImageRenderer(content: card)
renderer.scale = 3
renderer.isOpaque = false
if let img = renderer.uiImage {
    MarketingCapture.writePNG(img, name: "card-\(slugify(item.name))", subfolder: "elements")
}
```
Similar helpers are provided for widgets and charts.

## Known Gotchas
1. Live Activities persist across launches – end them at the start of capture.
2. Seed data only once; reseeding per locale can crash CloudKit sync.
3. ViewModels may capture an empty store before seeding – refresh after seeding.
4. Dismissing sheets via binding may fail – use a NotificationCenter signal.
5. NavigationPath cannot be popped externally – order captures accordingly.
6. Widget views live in an extension target – add them to the main app target or skip rendering.
7. `ProgressView` without style renders incorrectly – apply `.progressViewStyle(.linear)`.
8. `.containerBackground` is a no‑op outside widget context – wrap with explicit background.
9. iPhone 8 Plus is unavailable on iOS 26 simulators – use a modern device.
10. Locale launch arguments require parentheses: `-AppleLanguages (de) -AppleLocale de`.
11. `ImageRenderer` captures a single frame – add a delay for on‑appear animations.

## Output Layout
```
marketing/
    <locale>/
        01-home.png
        02‑detail.png
        …
        elements/
            card‑<name>.png
            widget‑<size>.png
            chart‑<name>.png
```
Add `marketing/` to `.gitignore`.

## Verification Checklist
- [ ] All locales contain the expected number of screenshots.
- [ ] Files differ between locales (translation applied).
- [ ] Visually inspect a few primary‑locale screens.
- [ ] Visually inspect the same screens for another locale.
- [ ] Verify at least one widget and one card render.
- [ ] No stray sheets or overlays appear in any screenshot.

## Templates
- `templates/MarketingCapture.swift.template` – skeleton for the capture file.
- `templates/capture-marketing.sh.template` – skeleton for the shell script (replace bundle ID, scheme, simulator).
