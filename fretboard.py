import tkinter as tk

# Notes for each string (standard tuning EADGBE), mirrored vertically
notes = ['E', 'B', 'G', 'D', 'A', 'E']  # High E string is now at the top, Low E is at the bottom

# All possible notes in a chromatic scale
chromatic_scale = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

def get_note_name(string_note, fret):
    """Returns the note name for a given string and fret."""
    start_index = chromatic_scale.index(string_note)
    return chromatic_scale[(start_index + fret) % len(chromatic_scale)]

def draw_fretboard(canvas, canvas_width, highlight_callback=None):
    """Draws the fretboard with 22 frets, 6 strings, note names, and inlays."""
    left_padding = 30  # Add padding to the left for the 0th fret notes
    string_spacing = 30
    canvas_height = string_spacing * 6 + 40
    normal_fret_width = (canvas_width - left_padding) // 22
    first_fret_width = normal_fret_width + 5
    fret_line_top = 50
    fret_line_bottom = canvas_height - 20

    canvas.config(width=canvas_width, height=canvas_height)

    # Fret inlays on frets 5, 7, 9, 12, 15, 17
    inlay_frets = [4, 6, 8, 14, 16]
    inlay_color = "black"
    inlay_radius = 5

    # Position the inlays outside the frets (below the fretboard)
    y_inlay_position = fret_line_bottom + 17  # Position below the frets

    # Draw single dot inlays between frets
    for fret in inlay_frets:
        x = left_padding + (fret + 0.5) * normal_fret_width + first_fret_width - normal_fret_width
        canvas.create_oval(x - inlay_radius, y_inlay_position - inlay_radius, x + inlay_radius, y_inlay_position + inlay_radius,
                           fill=inlay_color, outline="")

    # Double inlays for fret 12 with horizontal arrangement
    x_12 = left_padding + (11 + 0.5) * normal_fret_width + first_fret_width - normal_fret_width
    double_inlay_offset = 8
    canvas.create_oval(x_12 - inlay_radius - double_inlay_offset, y_inlay_position - inlay_radius,
                       x_12 + inlay_radius - double_inlay_offset, y_inlay_position + inlay_radius, fill=inlay_color, outline="")
    canvas.create_oval(x_12 - inlay_radius + double_inlay_offset, y_inlay_position - inlay_radius,
                       x_12 + inlay_radius + double_inlay_offset, y_inlay_position + inlay_radius, fill=inlay_color, outline="")

    # Draw frets
    canvas.create_line(left_padding, fret_line_top, left_padding, fret_line_bottom, width=15)  # Thicker 0th fret
    canvas.create_line(left_padding + first_fret_width, fret_line_top, left_padding + first_fret_width, fret_line_bottom, width=2)
    for i in range(2, 23):
        x = left_padding + first_fret_width + (i - 1) * normal_fret_width
        canvas.create_line(x, fret_line_top, x, fret_line_bottom, width=2)

    # Draw strings over the frets and inlays
    for i in range(6):
        canvas.create_line(left_padding, 50 + i * string_spacing, canvas_width, 50 + i * string_spacing, width=2)

    # Draw note names, move one fret to the left for correct positioning
    note_radius = 12
    for string in range(6):
        base_note = notes[string]
        y_pos = 50 + string * string_spacing
        for fret in range(22):
            if fret == 0:
                # Shift fret 0 notes as if they're on a "negative 1" fret
                x_pos = left_padding + first_fret_width - normal_fret_width - 20  # Further left for -1 fret effect
            else:
                # Adjust x_pos for notes to be one fret left
                x_pos = left_padding + first_fret_width + (fret - 1.5) * normal_fret_width

            note_name = get_note_name(base_note, fret)

            # Assign a tag to each note (circle + text) for easy selection later
            note_tag = f"note_{note_name}"

            # Draw circle for the note
            canvas.create_oval(x_pos - note_radius, y_pos - note_radius, x_pos + note_radius, y_pos + note_radius,
                               fill="dark grey", outline="", tags=note_tag)
            # Draw the note name in white
            canvas.create_text(x_pos, y_pos, text=note_name, fill="white", font=("Arial", 10, "bold"), tags=note_tag)

            if highlight_callback:
                canvas.tag_bind(note_tag, "<Button-1>", lambda event, note=note_name: handle_note_click(canvas, note, highlight_callback))


def handle_note_click(canvas, note, highlight_callback):
    """Handles note click event and sets the highlighted note."""
    # Store the clicked note as a variable to track it globally
    canvas.setvar("highlighted_note", note)
    highlight_callback(note)

def highlight_notes(canvas, root_note, intervals_to_highlight):
    """Highlights root note (red), major third (green), perfect fifth (blue), and major seventh (yellow) on the fretboard."""
    # Calculate the positions of intervals relative to the root note
    root_index = chromatic_scale.index(root_note)
    major_third_index = (root_index + 4) % 12  # Major third (M3) is 4 semitones above the root
    perfect_fifth_index = (root_index + 7) % 12  # Perfect fifth (P5) is 7 semitones above the root
    major_seventh_index = (root_index + 11) % 12  # Major seventh (M7) is 11 semitones above the root

    major_third = chromatic_scale[major_third_index]
    perfect_fifth = chromatic_scale[perfect_fifth_index]
    major_seventh = chromatic_scale[major_seventh_index]

    # Reset all note colors first
    for note in chromatic_scale:
        note_tag = f"note_{note}"
        # Reset both the circle fill and text color
        for item in canvas.find_withtag(note_tag):
            if canvas.type(item) == 'oval':
                canvas.itemconfig(item, fill="dark grey")  # Reset circle fill color
            elif canvas.type(item) == 'text':
                canvas.itemconfig(item, fill="white")  # Reset text color

    # Highlight root notes (red)
    if intervals_to_highlight.get('root', 0):
        root_tag = f"note_{root_note}"
        for item in canvas.find_withtag(root_tag):
            if canvas.type(item) == 'oval':
                canvas.itemconfig(item, fill="red")  # Highlight root note circle
            elif canvas.type(item) == 'text':
                canvas.itemconfig(item, fill="white")  # Keep the text color white

    # Highlight major third (green)
    if intervals_to_highlight.get('M3', 0):
        third_tag = f"note_{major_third}"
        for item in canvas.find_withtag(third_tag):
            if canvas.type(item) == 'oval':
                canvas.itemconfig(item, fill="green")  # Highlight M3 note circle
            elif canvas.type(item) == 'text':
                canvas.itemconfig(item, fill="white")  # Keep the text color white

    # Highlight perfect fifth (blue)
    if intervals_to_highlight.get('P5', 0):
        fifth_tag = f"note_{perfect_fifth}"
        for item in canvas.find_withtag(fifth_tag):
            if canvas.type(item) == 'oval':
                canvas.itemconfig(item, fill="blue")  # Highlight P5 note circle
            elif canvas.type(item) == 'text':
                canvas.itemconfig(item, fill="white")  # Keep the text color white

    # Highlight major seventh (orange)
    if intervals_to_highlight.get('M7', 0):
        seventh_tag = f"note_{major_seventh}"
        for item in canvas.find_withtag(seventh_tag):
            if canvas.type(item) == 'oval':
                canvas.itemconfig(item, fill="orange")  # Highlight M7 note circle
            elif canvas.type(item) == 'text':
                canvas.itemconfig(item, fill="white")  # Keep the text color white

    # Force UI update to immediately reflect changes
    canvas.update_idletasks()