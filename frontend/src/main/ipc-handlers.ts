import { ipcMain, BrowserWindow, app } from 'electron'

export function registerIpcHandlers(mainWindow: BrowserWindow): void {

    // Window Controls
    ipcMain.handle('window:minimize', () => {
        mainWindow.minimize()
    })

    ipcMain.handle('window:maximize', () => {
        if (mainWindow.isMaximized()) {
            mainWindow.unmaximize()
        } else {
            mainWindow.maximize()
        }
    })

    ipcMain.handle('window:close', () => {
        mainWindow.close()
    })

    // App Info
    ipcMain.handle('app:version', () => {
        return app.getVersion()
    })

    // System Stats Proxy (if needed distinct from WebSocket)
    ipcMain.handle('system:stats', async () => {
        // In future, can use node-os-utils here if backend is offline
        return {}
    })
}
