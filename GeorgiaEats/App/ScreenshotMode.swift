import Foundation
import CoreLocation
import UIKit

/// `-screenshot <name>` opens one screen with fixed state for App Store screenshots (scripts/capture-screenshots.sh).
/// Names: home, wings, buford, lowcountry, soul, honors, oldest, detail, map, saved, about.
enum ScreenshotMode {
    /// Debug builds only: an App Store build ignores the launch argument, so no one can reach seeded screens or fake locations.
    static var name: String? {
        #if DEBUG
        let args = ProcessInfo.processInfo.arguments
        guard let i = args.firstIndex(of: "-screenshot"), i + 1 < args.count else { return nil }
        return args[i + 1]
        #else
        return nil
        #endif
    }
    static var isActive: Bool { name != nil }

    @MainActor
    static func apply(to model: AppModel) {
        guard let name, model.isLoaded else { return }
        model.filters = Filters()
        // Midtown Atlanta (Peachtree St at 10th St), so "nearest" lists have distances without a permission prompt
        model.screenshotLocation = CLLocation(latitude: 33.7816, longitude: -84.3836)
        // by name and town, ignoring case, so a rebuild with a slightly different casing still finds the place; the hand-checked one first
        let pick = { (n: String, town: String?) -> Place? in
            let hits = model.places.filter { $0.name.caseInsensitiveCompare(n) == .orderedSame && (town == nil || $0.city == town) }
            return hits.first(where: \.handChecked) ?? hits.first
        }
        for p in [pick("The Busy Bee", "Atlanta"), pick("Miller Union", "Atlanta"), pick("Fishbar", "Savannah")]
            .compactMap({ $0 }) where !model.isSaved(p) {
            model.toggleSaved(p)
        }
        let open = { (g: Guide) in model.tab = .guides; model.selectedGuide = g; model.guidesPath = [.guide(g)] }
        switch name {
        case "wings": open(.wings)
        case "buford":
            // from Doraville (Buford Hwy at Shallowford Rd)
            model.screenshotLocation = CLLocation(latitude: 33.8987, longitude: -84.2833)
            open(.buford)
        case "lowcountry":
            // from downtown Savannah (Bull St at Broughton St)
            model.screenshotLocation = CLLocation(latitude: 32.0789, longitude: -81.0912)
            open(.lowcountry)
        case "soul": open(.soulFood)
        case "honors": open(.honors)
        case "oldest": open(.oldest)
        case "detail":
            // The Busy Bee on MLK Jr. Drive: hand-checked, a Bib Gourmand and an America's Classic, with its note
            open(.soulFood)
            if let p = pick("The Busy Bee", "Atlanta") ?? pick("Mary Mac's Tea Room", "Atlanta") ?? model.places.first {
                model.selectedPlace = p; model.guidesPath.append(.place(p))
            }
        case "map": model.tab = .map
        case "saved": model.tab = .saved
        case "about": model.tab = .about
        default: model.tab = .guides; model.selectedGuide = nil
        }
        // iPad shows the place column next to every list, so give each shot a place instead of "Pick a place": a different
        // honored or hand-checked one per shot.
        guard UIDevice.current.userInterfaceIdiom == .pad, model.selectedPlace == nil else { return }
        let place: Place? = switch name {
        case "home": pick("Mary Mac's Tea Room", "Atlanta")
        case "wings": pick("J.R. Crickets", "Atlanta")
        case "buford": pick("Han Il Kwan", "Doraville")
        case "lowcountry": pick("Fishbar", "Savannah")
        case "map": pick("Miller Union", "Atlanta")
        case "honors": pick("Bacchanalia", "Atlanta")
        case "oldest": pick("Majestic Diner", "Atlanta")   // the iPad set's sixth shot (the honors title truncates there)
        case "soul": pick("The Busy Bee", "Atlanta")
        case "saved": pick("Fishbar", "Savannah")
        case "about": nil
        default: pick("Heirloom Market BBQ", "Atlanta")
        }
        model.selectedPlace = place
    }
}
