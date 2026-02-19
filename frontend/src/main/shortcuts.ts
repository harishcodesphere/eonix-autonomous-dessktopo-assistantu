import { app, BrowserWindow, globalShortcut } from 'electron'

export function registerShortcuts(mainWindow: BrowserWindow): void {

    // Toggle Visibility: Alt+Space
    globalShortcut.register('Alt+Space', () => {
        if (mainWindow.isVisible()) {
            if (mainWindow.isFocused()) {
                mainWindow.hide()
            } else {
                mainWindow.show()
                mainWindow.focus()
            }
        } else {
            mainWindow.show()
            mainWindow.focus()
        }
    })

    // DevTools: Ctrl+Shift+I
    globalShortcut.register('CommandOrControl+Shift+I', () => {
        mainWindow.webContents.toggleDevTools()
    })
}

export function unregisterShortcuts(): void {
    globalShortcut.unregisterAll()
}
