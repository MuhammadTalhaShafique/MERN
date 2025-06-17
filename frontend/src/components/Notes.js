import React, { useEffect, useState } from "react";

function Notes({ token, onLogout }) {
  const [notes, setNotes] = useState([]);
  const [newNote, setNewNote] = useState("");

  const fetchNotes = async () => {
    const res = await fetch(`${process.env.REACT_APP_API_URL}/notes`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    setNotes(await res.json());
  };

  useEffect(() => {
    fetchNotes();
  }, [token]);

  const addNote = async () => {
    if (!newNote.trim()) return;
    await fetch(`${process.env.REACT_APP_API_URL}/notes`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({ text: newNote }),
    });
    setNewNote("");
    fetchNotes();
  };

  const delNote = async (id) => {
    await fetch(`${process.env.REACT_APP_API_URL}/notes/${id}`, {
      method: "DELETE",
      headers: { Authorization: `Bearer ${token}` },
    });
    fetchNotes();
  };

  return (
    <div>
      <h2>Your Notes</h2>
      <button onClick={onLogout}>Logout</button>
      <ul>
        {notes.map((note) => (
          <li key={note._id}>
            {note.text}
            <button onClick={() => delNote(note._id)}>Delete</button>
          </li>
        ))}
      </ul>
      <input
        value={newNote}
        onChange={(e) => setNewNote(e.target.value)}
        placeholder="Add new note"
      />
      <button onClick={addNote}>Add</button>
    </div>
  );
}

export default Notes;
