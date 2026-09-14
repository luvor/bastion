import Cocoa

struct BastionStatus: Decodable {
    let state: String
    let message: String?
    let updatedAt: String?
}

final class MenuBarController: NSObject, NSApplicationDelegate {
    private var statusItem: NSStatusItem!
    private var statusMenu: NSMenu!
    private var titleItem: NSMenuItem!
    private var detailItem: NSMenuItem!
    private var timer: Timer?
    private var animationTimer: Timer?
    private var animationFrames: [NSImage] = []
    private var animationIndex = 0

    private var statusURL: URL {
        if let raw = ProcessInfo.processInfo.environment["BASTION_STATUS_PATH"], !raw.isEmpty {
            return URL(fileURLWithPath: raw)
        }
        return FileManager.default.homeDirectoryForCurrentUser
            .appendingPathComponent("Library/Application Support/Bastion/status.json")
    }

    func applicationDidFinishLaunching(_ notification: Notification) {
        statusItem = NSStatusBar.system.statusItem(withLength: NSStatusItem.squareLength)
        statusItem.button?.toolTip = "Bastion Security"
        statusMenu = NSMenu()
        titleItem = NSMenuItem(title: "Bastion: checking…", action: nil, keyEquivalent: "")
        detailItem = NSMenuItem(title: "", action: nil, keyEquivalent: "")
        titleItem.isEnabled = false
        detailItem.isEnabled = false
        statusMenu.addItem(titleItem)
        statusMenu.addItem(detailItem)
        statusMenu.addItem(.separator())
        let scanItem = NSMenuItem(title: "Open Bastion status", action: #selector(openStatus), keyEquivalent: "")
        scanItem.target = self
        statusMenu.addItem(scanItem)
        statusMenu.addItem(.separator())
        let quitItem = NSMenuItem(title: "Quit Bastion mascot", action: #selector(quit), keyEquivalent: "q")
        quitItem.target = self
        statusMenu.addItem(quitItem)
        statusItem.menu = statusMenu

        loadAnimation()
        refresh()
        timer = Timer.scheduledTimer(withTimeInterval: 30, repeats: true) { [weak self] _ in self?.refresh() }
        animationTimer = Timer.scheduledTimer(withTimeInterval: 0.7, repeats: true) { [weak self] _ in self?.nextFrame() }
    }

    private func refresh() {
        guard let data = try? Data(contentsOf: statusURL),
              let status = try? JSONDecoder().decode(BastionStatus.self, from: data) else {
            set(state: "NOT CONFIGURED", detail: "Collector status is missing")
            return
        }
        set(state: status.state.uppercased(), detail: status.message ?? status.updatedAt ?? "Status available")
    }

    private func set(state: String, detail: String) {
        titleItem.title = "Bastion: (state)"
        detailItem.title = detail
        titleItem.attributedTitle = NSAttributedString(string: titleItem.title, attributes: [.font: NSFont.boldSystemFont(ofSize: 13)])
    }

    private func loadAnimation() {
        guard let path = ProcessInfo.processInfo.environment["BASTION_MASCOT_SHEET"],
              let source = NSImage(contentsOfFile: path),
              let cgImage = source.cgImage(forProposedRect: nil, context: nil, hints: nil) else { return }
        let frameWidth = cgImage.width / 6
        for index in 0..<6 {
            let rect = CGRect(x: index * frameWidth, y: 0, width: frameWidth, height: cgImage.height)
            guard let frame = cgImage.cropping(to: rect) else { continue }
            animationFrames.append(NSImage(cgImage: frame, size: NSSize(width: 18, height: 18)))
        }
        nextFrame()
    }

    private func nextFrame() {
        guard !animationFrames.isEmpty else { return }
        statusItem.button?.image = animationFrames[animationIndex]
        animationIndex = (animationIndex + 1) % animationFrames.count
    }

    @objc private func openStatus() {
        NSWorkspace.shared.open(statusURL.deletingLastPathComponent())
    }

    @objc private func quit() {
        NSApplication.shared.terminate(nil)
    }
}

let app = NSApplication.shared
let delegate = MenuBarController()
app.delegate = delegate
app.setActivationPolicy(.accessory)
app.run()
