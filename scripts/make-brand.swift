// Georgia Eats brand: the app icon (Nick's pick 2026-10-26: concept A of scripts/icon-concepts.swift, a whole Georgia peach with its
// leaf and stem, on pine; the shared Eats Ranked icon style, state-prompts/ICON-STYLE.md, no backing shape).
// Usage, from ga-eats/: swift scripts/make-brand.swift   -> GeorgiaEats/Resources/Assets.xcassets/AppIcon.appiconset/icon-1024.png,
// docs/ favicons and touch icons, docs/og.png. scripts/make-site.py draws the same mark as its inline SVG: change both together.
import AppKit
import CoreGraphics
import ImageIO
import UniformTypeIdentifiers

func rgb(_ hex: UInt32) -> CGColor {
    CGColor(srgbRed: CGFloat((hex >> 16) & 255) / 255, green: CGFloat((hex >> 8) & 255) / 255, blue: CGFloat(hex & 255) / 255, alpha: 1)
}
let PINE: UInt32 = 0x1F4D3A, CLAY: UInt32 = 0xA63D24, CREAM: UInt32 = 0xFFF8EE, PEACH: UInt32 = 0xF6A57A

/// A whole Georgia peach (front view), its cleft at the top, a deeper blush over the lower part, the suture, a stem and one leaf.
/// CoreGraphics y-up. Identical to icon-concepts.swift's concept A.
func peach(_ c: CGContext, _ s: CGFloat) {
    let dy: CGFloat = 0.03
    func P(_ x: CGFloat, _ y: CGFloat) -> CGPoint { CGPoint(x: x * s, y: (y + dy) * s) }
    let body = CGMutablePath()
    body.move(to: P(0.50, 0.700))
    body.addCurve(to: P(0.835, 0.455), control1: P(0.565, 0.765), control2: P(0.835, 0.735))
    body.addCurve(to: P(0.50, 0.135), control1: P(0.835, 0.245), control2: P(0.69, 0.135))
    body.addCurve(to: P(0.165, 0.455), control1: P(0.31, 0.135), control2: P(0.165, 0.245))
    body.addCurve(to: P(0.50, 0.700), control1: P(0.165, 0.735), control2: P(0.435, 0.765))
    body.closeSubpath()
    // leaf first (it tucks behind the shoulder), then the stem
    let leaf = CGMutablePath()
    leaf.move(to: P(0.515, 0.735))
    leaf.addQuadCurve(to: P(0.76, 0.845), control: P(0.58, 0.885))
    leaf.addQuadCurve(to: P(0.515, 0.735), control: P(0.70, 0.715))
    leaf.closeSubpath()
    c.setFillColor(rgb(0x7DAF45)); c.addPath(leaf); c.fillPath()
    c.setStrokeColor(rgb(0x6B4A2E)); c.setLineWidth(0.040 * s); c.setLineCap(.round)
    c.move(to: P(0.50, 0.70)); c.addLine(to: P(0.515, 0.79)); c.strokePath()
    c.setFillColor(rgb(PEACH)); c.addPath(body); c.fillPath()
    // the blush: a deeper tone over the lower part, hard curved edge
    c.saveGState(); c.addPath(body); c.clip()
    c.setFillColor(rgb(0xE07B53)); c.fillEllipse(in: CGRect(x: 0.02 * s, y: (-0.20 + dy) * s, width: 0.96 * s, height: 0.62 * s))
    c.restoreGState()
    // the suture from the cleft down the left cheek (one mark)
    c.setStrokeColor(rgb(0xE07B53)); c.setLineWidth(0.036 * s); c.setLineCap(.round)
    c.move(to: P(0.50, 0.675)); c.addQuadCurve(to: P(0.445, 0.43), control: P(0.425, 0.58)); c.strokePath()
}

func render(_ n: Int, _ path: String, background: Bool) {
    let ctx = CGContext(data: nil, width: n, height: n, bitsPerComponent: 8, bytesPerRow: 0, space: CGColorSpace(name: CGColorSpace.sRGB)!,
                        bitmapInfo: background ? CGImageAlphaInfo.noneSkipLast.rawValue : CGImageAlphaInfo.premultipliedLast.rawValue)!
    ctx.setShouldAntialias(true)
    if background { ctx.setFillColor(rgb(PINE)); ctx.fill(CGRect(x: 0, y: 0, width: n, height: n)) }
    peach(ctx, CGFloat(n))
    let d = CGImageDestinationCreateWithURL(URL(fileURLWithPath: path) as CFURL, UTType.png.identifier as CFString, 1, nil)!
    CGImageDestinationAddImage(d, ctx.makeImage()!, nil)
    guard CGImageDestinationFinalize(d) else { fatalError("could not write \(path)") }
    print("wrote", path)
}
render(1024, "GeorgiaEats/Resources/Assets.xcassets/AppIcon.appiconset/icon-1024.png", background: true)
try? FileManager.default.createDirectory(atPath: "docs", withIntermediateDirectories: true)
for (n, name) in [(512, "icon-512.png"), (192, "icon-192.png"), (180, "apple-touch-icon.png"), (32, "favicon-32.png")] {
    render(n, "docs/" + name, background: true)
}

/// The share image (1200 x 630): pine, the peach at the left, the name and tagline at the right, and the app's header band along the
/// bottom: a row of longleaf pines over a red-clay strip.
func og(_ path: String) {
    let W = 1200, H = 630
    let ctx = CGContext(data: nil, width: W, height: H, bitsPerComponent: 8, bytesPerRow: 0, space: CGColorSpace(name: CGColorSpace.sRGB)!,
                        bitmapInfo: CGImageAlphaInfo.noneSkipLast.rawValue)!
    ctx.setShouldAntialias(true)
    ctx.setFillColor(rgb(PINE)); ctx.fill(CGRect(x: 0, y: 0, width: W, height: H))
    ctx.setFillColor(rgb(CLAY)); ctx.fill(CGRect(x: 0, y: 0, width: W, height: 26))
    ctx.setFillColor(rgb(0x163A2B))
    var x: CGFloat = 0
    while x < CGFloat(W) {
        ctx.move(to: CGPoint(x: x, y: 26)); ctx.addLine(to: CGPoint(x: x + 14, y: 62)); ctx.addLine(to: CGPoint(x: x + 28, y: 26)); ctx.closePath(); ctx.fillPath()
        x += 36
    }
    ctx.saveGState(); ctx.translateBy(x: 30, y: 70); peach(ctx, 520); ctx.restoreGState()
    let ns = NSGraphicsContext(cgContext: ctx, flipped: false)
    NSGraphicsContext.saveGraphicsState(); NSGraphicsContext.current = ns
    let title = NSFont(name: "AvenirNextCondensed-Heavy", size: 92) ?? NSFont.boldSystemFont(ofSize: 80)
    let sub = NSFont(name: "AvenirNextCondensed-DemiBold", size: 38) ?? NSFont.boldSystemFont(ofSize: 34)
    NSAttributedString(string: "GEORGIA EATS", attributes: [.font: title, .foregroundColor: NSColor.white]).draw(at: NSPoint(x: 580, y: 330))
    NSAttributedString(string: "WINGS, BARBECUE & LOWCOUNTRY", attributes: [.font: sub, .foregroundColor: NSColor(srgbRed: 0.965, green: 0.647, blue: 0.478, alpha: 1)]).draw(at: NSPoint(x: 584, y: 272))
    NSGraphicsContext.restoreGraphicsState()
    let d = CGImageDestinationCreateWithURL(URL(fileURLWithPath: path) as CFURL, UTType.png.identifier as CFString, 1, nil)!
    CGImageDestinationAddImage(d, ctx.makeImage()!, nil)
    guard CGImageDestinationFinalize(d) else { fatalError("could not write \(path)") }
    print("wrote", path)
}
og("docs/og.png")
