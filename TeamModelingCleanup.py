"""
Author - Kat Feingold, HEC
Date - 7/1/20025
Changes: 
Script creation
Recursively deletes all files named ".block.revision.dss" beneath a selected directory
displays a pop for watershed folder selection
pops up “Done” when finished
"""
#imports
import os, threading
from javax.swing import (
    UIManager, JFileChooser, JOptionPane, JDialog,
    JProgressBar, JPanel, JLabel, SwingUtilities
)
from javax.swing import WindowConstants
from java.awt import BorderLayout

# this will delete anything that ends in the .block.revision.dss
SUFFIX = ".block.revision.dss"

def choose_directory(title="Select Master Watershed Folder"):
    try:
        UIManager.setLookAndFeel(UIManager.getSystemLookAndFeelClassName())
    except:
        pass
    chooser = JFileChooser()
    chooser.setDialogTitle(title)
    chooser.setFileSelectionMode(JFileChooser.DIRECTORIES_ONLY)
    chooser.setAcceptAllFileFilterUsed(False)
    if chooser.showOpenDialog(None) == JFileChooser.APPROVE_OPTION:
        return str( chooser.getSelectedFile().getAbsolutePath() )
    return None

def main():
    root = choose_directory()
    if not root:
        return
    if not os.path.isdir(root):
        JOptionPane.showMessageDialog(
            None,
            "Not a directory:\n" + root,
            "Error", JOptionPane.ERROR_MESSAGE
        )
        return

    resp = JOptionPane.showConfirmDialog(
        None,
        "Delete *all* files ending with\n  %s\nunder:\n  %s\nProceed?" % (SUFFIX, root),
        "Confirm Deletion",
        JOptionPane.YES_NO_OPTION, JOptionPane.WARNING_MESSAGE
    )
    if resp != JOptionPane.YES_OPTION:
        return

    # displays throbber to show user script is running in case it runs for a while
    dlg = JDialog(None, "Deleting “%s” files…" % SUFFIX)
    dlg.setModal(False)
    dlg.setDefaultCloseOperation(WindowConstants.DO_NOTHING_ON_CLOSE)
    bar = JProgressBar(); bar.setIndeterminate(True)
    pnl = JPanel(BorderLayout(5,5))
    pnl.add(JLabel("Please wait…"), BorderLayout.NORTH)
    pnl.add(bar, BorderLayout.CENTER)
    dlg.getContentPane().add(pnl)
    dlg.pack()
    dlg.setLocationRelativeTo(None)
    dlg.setVisible(True)

    def worker():
        deleted = 0
        for dirpath, _, files in os.walk(root):
            for fn in files:
                name = str(fn)
                low = name.lower()
                
                print "Considering:", os.path.join(dirpath, name)
                if low.endswith(SUFFIX):
                    full = os.path.join(dirpath, name)
                    try:
                        os.remove(full)
                        deleted += 1
                        print "Deleting:", full
                    except Exception, e:
                        print "ERROR deleting %s: %s" % (full, e)
        # turns off the throbber and gives user a "done" dialog with number of files deleted
        SwingUtilities.invokeLater(lambda: dlg.dispose())
        SwingUtilities.invokeLater(lambda: JOptionPane.showMessageDialog(
            None,
            "Done! %d file(s) deleted." % deleted,
            "Finished", JOptionPane.INFORMATION_MESSAGE
        ))

    t = threading.Thread(target=worker)
    t.setDaemon(True)
    t.start()

if __name__ == "__main__":
    main()