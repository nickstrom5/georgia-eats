import SwiftUI

struct AboutView: View {
    @Environment(AppModel.self) private var model

    var body: some View {
        List {
            Section {
                VStack(alignment: .leading, spacing: 8) {
                    Text("GEORGIA EATS").displayFont(32).foregroundStyle(Theme.green)
                    Text("A free guide to \(model.restaurantCount.formatted()) Georgia restaurants, with MICHELIN and James Beard honors, the state's alcohol licenses, and hand-checked lists of Georgia's own food as they're checked. No account, no ads, no tracking.")
                        .font(.subheadline).foregroundStyle(Theme.ink2)
                    Text("Georgia Eats is an independent app by Nicholas Soderstrom. It is not affiliated with, endorsed by or operated by the State of Georgia, the Georgia Department of Revenue, the Georgia Department of Public Health, GNR Public Health, Fulton County or any county health department, Georgia Tourism, the MICHELIN Guide, the James Beard Foundation, Apple, or any restaurant or chain. Other names are trademarks of their owners.")
                        .font(.footnote).foregroundStyle(Theme.muted)
                }
                .padding(.vertical, 4)
            }
            Section("How the lists are built") {
                Text("Hand-checked lists (meat-and-threes and soul food, Buford Highway, lemon pepper wings, barbecue and Brunswick stew, Lowcountry seafood, peach cobbler, Georgia-born chains, oldest places) include only places checked against a 2025 or 2026 source (the place's own website or menu, local news or an official tourism listing), with the address checked. Founding years mean the year it opened at this address.")
                Text("Honors are the MICHELIN Guide American South's 2026 Georgia selection (ten one-star restaurants, Bib Gourmands and recommended places), James Beard Foundation winners, 2025 and 2026 nominees and semifinalists, and America's Classics.")
                Text("Georgia publishes no list of its restaurants. This app starts from open map listings (Overture Maps) and keeps the kinds that proved reliable: checked against Fulton County's food service permits and the state's alcohol licenses, high-confidence listings matched far more often than the kinds left out. The Department of Revenue's alcohol licenses confirm places statewide, say which may serve alcohol, and add ones the map data missed. A place with no matching state license is shown as unknown, never as dry: cities and counties license too. Adult clubs are left out. Website links are checked, and any that no longer belong to the place are left out.")
                Text("County health departments inspect restaurants under the Georgia Department of Public Health's Food Service Rules. Each report has a 0 to 100 score and an official letter grade (A 90–100, B 80–89, C 70–79, U 69 or below), posted near the entrance. Reports are published only in DPH's search (and GNR Public Health's, for Gwinnett, Newton and Rockdale), not as data, so this app shows no scores and computes no grade; each place links to the search.")
                Text("Ratings, reviews, hours and photos are Apple Maps' own, shown live in Apple's place card. This app doesn't store or rank by them.")
            }
            .font(.subheadline).foregroundStyle(Theme.ink2)
            Section("Sources") {
                source("Georgia Department of Revenue", "Active Alcohol Licenses, the department's quarterly report (\(model.permitsUpdated)), modified for use in this app. In the department's words, the report \u{201C}reflects all active licenses issued and/or assigned numbers to entities pending issuance.\u{201D} No approval by the department is claimed.", Links.alcoholLicenses.absoluteString)
                source("Georgia Department of Public Health", "Inspection reports and letter grades for every county but Gwinnett, Newton and Rockdale, in the department's own search. Linked from each place; not copied. The grade bands are from its Food Service Rules, Ga. Comp. R. & Regs. 511-6-1-.10.", Links.inspections.absoluteString)
                source("GNR Public Health", "Inspection reports for Gwinnett, Newton and Rockdale counties, in the district's own search. Linked from those places; not copied.", Links.gnrHealth.absoluteString)
                source("Fulton County Government", "Food Service Inspections (data.fultoncountyga.gov), Creative Commons Attribution 4.0. Used only to measure how often each kind of map listing matched a permit the county inspected in 2020–21; no inspection result is shown.", "https://data.fultoncountyga.gov/d/w896-7wba")
                source("Overture Maps Foundation", "Restaurant listings and websites come from Overture Maps Foundation places data (overturemaps.org)\(model.overtureRelease.map { ", release \($0)" } ?? ""), filtered and reformatted for this app.\n• Data from Meta, Microsoft, DAC and BrightQuery. Available under CDLA Permissive 2.0.\n• Data from Foursquare. \(foursquareCopyright) Available under Apache 2.0. Foursquare data was transformed to the Overture schema; this app further filtered and reformatted it. See the NOTICE below.\n• Data from AllThePlaces. Available under CC0 1.0.\nResearched places are put on the map with Overture Maps addresses data (open address sources under permissive licenses, docs.overturemaps.org/attribution).", "https://overturemaps.org")
                source("Honors", "The MICHELIN Guide American South selection and James Beard Foundation awards, nominees, semifinalists and America's Classics are reported as facts and checked by hand against the official announcements. MICHELIN and the MICHELIN Guide are trademarks of Michelin. James Beard Foundation and James Beard Award are trademarks of the James Beard Foundation. Other names belong to their owners.", "https://guide.michelin.com/us/en/georgia/restaurants")
                source("Maps", "Maps, place cards and directions by Apple Maps.", nil)
            }
            Section("Licenses") {
                NavigationLink("Community Data License Agreement – Permissive 2.0") { LicenseText(file: "CDLA-Permissive-2.0", title: "CDLA Permissive 2.0") }
                NavigationLink("Apache License 2.0") { LicenseText(file: "Apache-2.0", title: "Apache License 2.0") }
                NavigationLink("Foursquare OS Places NOTICE") { LicenseText(file: "Foursquare-NOTICE", title: "Foursquare NOTICE") }
            }
            Section("Privacy") {
                Text("The app collects nothing. Your location, if you allow it, only sorts lists by distance and shows where you are on the map, on this device. Saved places stay on this device.")
                    .font(.subheadline).foregroundStyle(Theme.ink2)
                DataUpdatesNote()
                    .font(.footnote).foregroundStyle(Theme.muted)
                Link("Privacy policy", destination: Links.privacy)
                Link("Terms of use", destination: Links.terms)
            }
            Section("Help") {
                Link("Report a missing or closed place", destination: Links.correctionEmail)
                Link("Email \(Links.supportEmail)", destination: URL(string: "mailto:\(Links.supportEmail)")!)
                Link("Website", destination: Links.site)
                Text("Data as of \(DayFormat.text(model.generated) ?? model.generated). Places open and close; check before you go. Version \(Bundle.main.object(forInfoDictionaryKey: "CFBundleShortVersionString") as? String ?? "1.0")")
                    .font(.footnote).foregroundStyle(Theme.muted)
            }
        }
        .navigationTitle("About")
        .tint(Theme.green)
    }

    /// the copyright line exactly as the bundled Foursquare NOTICE has it, so the two can't disagree
    private var foursquareCopyright: String {
        guard let url = Bundle.main.url(forResource: "Foursquare-NOTICE", withExtension: "txt"),
              let text = try? String(contentsOf: url, encoding: .utf8),
              let line = text.split(separator: "\n").first(where: { $0.hasPrefix("©") }) else { return "© Foursquare Labs, Inc. All rights reserved." }
        return line.trimmingCharacters(in: .whitespaces)
    }

    @ViewBuilder
    private func source(_ name: String, _ detail: String, _ url: String?) -> some View {
        VStack(alignment: .leading, spacing: 2) {
            if let url, let u = URL(string: url) { Link(name, destination: u).font(.subheadline.weight(.semibold)) }
            else { Text(name).font(.subheadline.weight(.semibold)) }
            Text(detail).font(.caption).foregroundStyle(Theme.muted)
        }
    }
}

/// A bundled license text (Resources/Licenses), reflowed rather than shown as raw 80-column lines.
struct LicenseText: View {
    let file: String
    let title: String

    var body: some View {
        ScrollView {
            Text(text).font(.footnote).foregroundStyle(Theme.ink).textSelection(.enabled)
                .frame(maxWidth: .infinity, alignment: .leading).padding()
        }
        .inlineTitle(title)
    }

    private var text: String {
        guard let url = Bundle.main.url(forResource: file, withExtension: "txt"),
              let raw = try? String(contentsOf: url, encoding: .utf8) else { return "License text missing." }
        // join hard-wrapped lines into paragraphs; keep blank lines and list items as breaks
        var out: [String] = []
        for para in raw.components(separatedBy: "\n\n") {
            let lines = para.components(separatedBy: "\n").map { $0.trimmingCharacters(in: .whitespaces) }
            var joined = ""
            for l in lines where !l.isEmpty {
                let startsItem = l.hasPrefix("–") || l.hasPrefix("-") || l.range(of: #"^\(?[a-z0-9]{1,3}[.)]\s"#, options: .regularExpression) != nil
                joined += joined.isEmpty ? l : (startsItem ? "\n" + l : " " + l)
            }
            if !joined.isEmpty { out.append(joined) }
        }
        return out.joined(separator: "\n\n")
    }
}
