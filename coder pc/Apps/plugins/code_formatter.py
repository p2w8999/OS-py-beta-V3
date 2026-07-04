
"""Example plugin - Code Formatter"""
import tkinter.messagebox as messagebox

def run(ide):
    """Run the plugin - gets called with the IDE instance"""
    content = ide.text_area.get("1.0", "end")
    # Simple formatting: strip trailing whitespace
    lines = content.split("\n")
    formatted = [line.rstrip() for line in lines]
    formatted_content = "\n".join(formatted)
    ide.text_area.delete("1.0", "end")
    ide.text_area.insert("1.0", formatted_content)
    messagebox.showinfo("Success", "Code formatted! Trailing whitespace removed.")
