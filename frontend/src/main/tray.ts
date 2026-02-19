import { Tray, Menu, nativeImage, BrowserWindow, app } from 'electron'
import { join } from 'path'
// @ts-ignore
import icon from '../../resources/icon.png?asset'

let tray: Tray | null = null

export function createTray(mainWindow: BrowserWindow): void {
    const iconImage = nativeImage.createFromPath(icon) // In real app, verify path
    tray = new Tray(iconImage)

    const contextMenu = Menu.buildFromTemplate([
        {
            label: 'Show Eonix',
            click: () => mainWindow.show()
        },
        { type: 'separator' },
        {
            label: 'Quit',
            click: () => app.quit()
        }
    ])

    tray.setToolTip('Eonix AI')
    tray.setContextMenu(contextMenu)

    tray.on('double-click', () => {
        if (mainWindow.isVisible()) {
            mainWindow.hide()
        } else {
            mainWindow.show()
        }
    })
}
