// backend/src/routes/source.routes.js
import express from "express";
import {
  getAllSources,
  getSourceById
} from "../controllers/source.controller.js";

const router = express.Router();

router.get("/", getAllSources);
router.get("/:id", getSourceById);

export default router;