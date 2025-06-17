const express = require("express");
const Note = require("../models/Note");
const auth = require("../middleware/auth");
const router = express.Router();

// Get all notes for user
router.get("/", auth, async (req, res) => {
  const notes = await Note.find({ userId: req.user.id });
  res.json(notes);
});

// Add note
router.post("/", auth, async (req, res) => {
  const note = new Note({ userId: req.user.id, text: req.body.text });
  await note.save();
  res.json(note);
});

// Delete note
router.delete("/:id", auth, async (req, res) => {
  await Note.deleteOne({ _id: req.params.id, userId: req.user.id });
  res.json({ success: true });
});

module.exports = router;
