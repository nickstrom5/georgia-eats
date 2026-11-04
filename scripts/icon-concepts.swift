// Georgia icon concepts for Nick's pick, in the shared Eats Ranked icon style (state-prompts/ICON-STYLE.md v1):
// one flat, level, centred food on a plain background; no scenery, tilt, texture, gloss or gradients.
// Usage (from ga-eats/): swift scripts/icon-concepts.swift   -> playbook/brand/concept-{a,b,c}-1024.png and -512, -180, -60 copies
//   A  a whole Georgia peach with its leaf, on pine
//   B  a peanut in the shell, on Georgia clay
//   C  a cast-iron skillet of peach cobbler seen from above (biscuit drops on peaches), on cream
// Palette (the prompt's landscape option): pine #1F4D3A, Georgia clay #A63D24, cream #FFF8EE, peach #F6A57A (a fill, never text).
// Food-only tones are listed per concept.
import AppKit
import CoreGraphics
import ImageIO
import UniformTypeIdentifiers

func rgb(_ hex: UInt32) -> CGColor {
    CGColor(srgbRed: CGFloat((hex >> 16) & 255) / 255, green: CGFloat((hex >> 8) & 255) / 255, blue: CGFloat(hex & 255) / 255, alpha: 1)
}
let PINE: UInt32 = 0x1F4D3A, CLAY: UInt32 = 0xA63D24, CREAM: UInt32 = 0xFFF8EE, PEACH: UInt32 = 0xF6A57A

// MARK: A, a whole peach (front view: a round fruit), its cleft at the top, a deeper blush over the lower part (light from above),
// the suture as one round-cap stroke, a short stem and one leaf. CoreGraphics y-up.
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

// MARK: B, a peanut in the shell (long food: side elevation): two lobes and a waist, a lighter top plane, a darker underside,
// and the shell's lengthwise ridges as six round-cap strokes in the underside tone.
func peanut(_ c: CGContext, _ s: CGFloat) {
    func P(_ x: CGFloat, _ y: CGFloat) -> CGPoint { CGPoint(x: x * s, y: y * s) }
    let shell = CGMutablePath()
    shell.addEllipse(in: CGRect(x: 0.145 * s, y: 0.305 * s, width: 0.355 * s, height: 0.355 * s))      // left lobe, r 0.1775 at (0.3225, 0.4825)
    shell.addEllipse(in: CGRect(x: 0.475 * s, y: 0.30 * s, width: 0.38 * s, height: 0.38 * s))          // right lobe, r 0.19 at (0.665, 0.49)
    shell.addRoundedRect(in: CGRect(x: 0.32 * s, y: 0.37 * s, width: 0.35 * s, height: 0.24 * s), cornerWidth: 0.10 * s, cornerHeight: 0.10 * s)
    c.setFillColor(rgb(0xE2B272)); c.addPath(shell); c.fillPath()
    c.saveGState(); c.addPath(shell); c.clip()
    c.setFillColor(rgb(0xEFCB93)); c.fill(CGRect(x: 0, y: 0.585 * s, width: s, height: s))     // up-facing plane
    c.setFillColor(rgb(0xC48D4B)); c.fill(CGRect(x: 0, y: 0, width: s, height: 0.385 * s))     // underside
    c.restoreGState()
    // ridges: three short arcs on each lobe
    c.setStrokeColor(rgb(0xC48D4B)); c.setLineWidth(0.036 * s); c.setLineCap(.round)
    for (cx, cy, r) in [(0.3225, 0.4825, 0.1775), (0.665, 0.49, 0.19)] as [(CGFloat, CGFloat, CGFloat)] {
        for off in [-0.07, 0.0, 0.07] as [CGFloat] {
            let y = cy + off
            let half = sqrt(max(0, r * r - off * off)) * 0.55
            c.move(to: P(cx - half, y)); c.addQuadCurve(to: P(cx + half, y), control: P(cx, y + 0.025)); c.strokePath()
        }
    }
}

// MARK: C, a cast-iron skillet of peach cobbler from above (a round dish recognised from the top): the iron pan and handle,
// the peach filling, and five golden biscuit drops on it. The handle's hang hole cuts through to the background.
func cobbler(_ c: CGContext, _ s: CGFloat) {
    let cx: CGFloat = 0.425, cy: CGFloat = 0.49, r: CGFloat = 0.29
    func R(_ x: CGFloat, _ y: CGFloat, _ w: CGFloat, _ h: CGFloat) -> CGRect { CGRect(x: x * s, y: y * s, width: w * s, height: h * s) }
    c.setFillColor(rgb(0x2E2A28))
    let handle = CGPath(roundedRect: R(cx + r - 0.03, cy - 0.05, 0.18, 0.10), cornerWidth: 0.05 * s, cornerHeight: 0.05 * s, transform: nil)
    c.addPath(handle); c.fillPath()
    c.fillEllipse(in: R(cx - r, cy - r, 2 * r, 2 * r))
    c.setFillColor(rgb(CREAM)); c.fillEllipse(in: R(cx + r + 0.075, cy - 0.024, 0.048, 0.048))
    let ri = r - 0.05
    c.setFillColor(rgb(0xE07B53)); c.fillEllipse(in: R(cx - ri, cy - ri, 2 * ri, 2 * ri))
    // biscuit drops: four round the edge and one in the middle, each a golden disc with a lighter up-facing top
    for (dx, dyy, d) in [(0.0, 0.0, 0.15), (-0.112, 0.095, 0.135), (0.112, 0.095, 0.135), (-0.112, -0.095, 0.135), (0.112, -0.095, 0.135)] as [(CGFloat, CGFloat, CGFloat)] {
        c.setFillColor(rgb(0xE9B86A)); c.fillEllipse(in: R(cx + dx - d / 2, cy + dyy - d / 2, d, d))
    }
}

// MARK: - main
let root = URL(fileURLWithPath: CommandLine.arguments[0]).deletingLastPathComponent().deletingLastPathComponent().path
let out = root + "/playbook/brand"
try? FileManager.default.createDirectory(atPath: out, withIntermediateDirectories: true)
func canvas(_ n: Int) -> CGContext {
    let c = CGContext(data: nil, width: n, height: n, bitsPerComponent: 8, bytesPerRow: 0,
                      space: CGColorSpace(name: CGColorSpace.sRGB)!, bitmapInfo: CGImageAlphaInfo.noneSkipLast.rawValue)!
    c.setAllowsAntialiasing(true); c.setShouldAntialias(true); c.interpolationQuality = .high
    return c
}
func save(_ img: CGImage, _ name: String) {
    let dest = CGImageDestinationCreateWithURL(URL(fileURLWithPath: out + "/" + name) as CFURL, UTType.png.identifier as CFString, 1, nil)!
    CGImageDestinationAddImage(dest, img, nil)
    guard CGImageDestinationFinalize(dest) else { fatalError("could not write \(name)") }
}
for (key, bg, draw) in [("a", PINE, peach), ("b", CLAY, peanut), ("c", CREAM, cobbler)] as [(String, UInt32, (CGContext, CGFloat) -> Void)] {
    let c = canvas(1024)
    c.setFillColor(rgb(bg)); c.fill(CGRect(x: 0, y: 0, width: 1024, height: 1024))
    draw(c, 1024)
    let full = c.makeImage()!
    save(full, "concept-\(key)-1024.png")
    for n in [512, 180, 60] {
        let sm = canvas(n); sm.draw(full, in: CGRect(x: 0, y: 0, width: n, height: n)); save(sm.makeImage()!, "concept-\(key)-\(n).png")
    }
    print("wrote concept-\(key)")
}
