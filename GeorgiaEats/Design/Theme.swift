import SwiftUI
import UIKit
import CoreText

/// Georgia landscape palette (Nick's pick, 2026-10-26), light only: pine #1F4D3A (9.6:1 on white) for titles, tint and accents;
/// Georgia clay #A63D24 (6.3:1 on white, white on it 6.3:1) for the hand-checked Georgia guide cards under white text and for MICHELIN
/// chips; peach #F6A57A only as a pin and card fill under dark text (white on peach is 2.0:1, so never text on it); cream #FFF8EE
/// surfaces. Neutral between Georgia and Georgia Tech fans: no team colors. The names `green`/`gold` are kept from Wisconsin Eats so
/// the shared views read the same; here `green` is pine and `gold` is clay.
enum Theme {
    static let green = Color(hex: 0x1F4D3A)      // pine: titles, tint, primary text accents
    static let green2 = Color(hex: 0x2E6650)
    static let gold = Color(hex: 0xA63D24)       // Georgia clay: card fills under white text, chips
    static let goldSoft = Color(hex: 0xFBE0D0)   // soft clay
    static let lime = Color(hex: 0xF6A57A)       // peach, fills only (hand-checked pins), under dark text
    static let limeSoft = Color(hex: 0xFDE3CF)
    static let sand = Color(hex: 0xFFF8EE)       // the Home background, cream
    static let red = Color(hex: 0xA63D24)        // MICHELIN chips
    static let ink = Color(hex: 0x16261F)
    static let ink2 = Color(hex: 0x2F4239)
    static let muted = Color(hex: 0x56635C)
    static let surface = Color.white
    static let surface2 = Color(hex: 0xF7F1E7)
    static let surface3 = Color(hex: 0xECE3D6)
    static let rule = Color(hex: 0xECE3D6)
    static let rule2 = Color(hex: 0xD4C6B2)
}

extension Color {
    init(hex: UInt32) {
        self.init(red: Double((hex >> 16) & 0xFF) / 255, green: Double((hex >> 8) & 0xFF) / 255, blue: Double(hex & 0xFF) / 255)
    }
}

/// A small uppercase label: "STONE CRAB", "1 MICHELIN STAR".
struct Chip: View {
    enum Style { case gold, green, red, plain, dashed }
    let text: String
    var style: Style = .plain

    var body: some View {
        Text(text.uppercased())
            .font(.caption2.weight(.bold))
            .tracking(0.4)
            .padding(.horizontal, 7).padding(.vertical, 3)
            .foregroundStyle(style == .green || style == .red ? Color.white : style == .dashed ? Theme.muted : style == .gold ? Theme.ink : Theme.green)
            .background {
                RoundedRectangle(cornerRadius: 5).fill(style == .gold ? Theme.goldSoft : style == .green ? Theme.green : style == .red ? Theme.red
                                                       : style == .dashed ? .clear : Theme.surface2)
            }
            .overlay {
                if style == .dashed { RoundedRectangle(cornerRadius: 5).strokeBorder(Theme.rule2, style: StrokeStyle(lineWidth: 1, dash: [3, 2])) }
            }
            .accessibilityLabel(text)
    }
}

/// Georgia Eats' lettering: the system face drawn compressed and heavy for titles and guide names (like a show poster), and the
/// system monospaced face for numbers, dates and small labels. No bundled fonts.
struct DisplayFont: ViewModifier {
    let size: CGFloat
    var weight: Font.Weight = .black
    @ScaledMetric(relativeTo: .body) private var scale: CGFloat = 1

    func body(content: Content) -> some View {
        content.font(.system(size: size * min(scale, 1.6), weight: weight).width(.compressed))
    }
}

/// Numbers, dates and small labels in the system monospaced face, scaled like DisplayFont.
struct MonoFont: ViewModifier {
    let size: CGFloat
    var weight: Font.Weight = .semibold
    @ScaledMetric(relativeTo: .body) private var scale: CGFloat = 1

    func body(content: Content) -> some View {
        content.font(.system(size: size * min(scale, 1.6), weight: weight, design: .monospaced))
    }
}

extension View {
    func displayFont(_ size: CGFloat, weight: Font.Weight = .black) -> some View {
        modifier(DisplayFont(size: size, weight: weight))
    }

    func monoFont(_ size: CGFloat, weight: Font.Weight = .semibold) -> some View {
        modifier(MonoFont(size: size, weight: weight))
    }
}

/// The band under the Home title: a red-clay band under a row of longleaf pines (Nick's pick, 2026-10-26).
struct Stripes: View {
    var height: CGFloat = 6

    var body: some View {
        Canvas { ctx, size in
            let w = size.width, h = size.height, band = max(3, h * 0.28)
            let tree = max(10, h * 0.62), step = tree * 1.25
            var x: CGFloat = 0
            while x < w {
                var p = Path()
                p.move(to: CGPoint(x: x, y: h - band))
                p.addLine(to: CGPoint(x: x + tree / 2, y: max(0, h - band - tree * 1.15)))
                p.addLine(to: CGPoint(x: x + tree, y: h - band))
                p.closeSubpath()
                ctx.fill(p, with: .color(Theme.green))
                x += step
            }
            ctx.fill(Path(CGRect(x: 0, y: h - band, width: w, height: band)), with: .color(Theme.gold))
        }
        .frame(height: height * 3.4)
        .clipShape(RoundedRectangle(cornerRadius: 3))
        .accessibilityHidden(true)
    }
}

extension View {
    /// An inline navigation title in the display type. UINavigationBar.appearance() didn't reach every SwiftUI bar on iOS 27
    /// (the Map title went from compressed blue to plain black after a push and pop; place titles were always plain), so the
    /// title is our own view in the bar. The navigation title is still set, for the back button and VoiceOver.
    func inlineTitle(_ title: String) -> some View {
        navigationTitle(title)
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .principal) {
                    Text(title).displayFont(19, weight: .heavy).foregroundStyle(Theme.green)
                        .lineLimit(1).minimumScaleFactor(0.7)
                        .accessibilityAddTraits(.isHeader)
                }
            }
    }
}
