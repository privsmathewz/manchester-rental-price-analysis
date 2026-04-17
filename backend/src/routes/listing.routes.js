// backend/src/routes/listing.routes.js
import express from "express";
import {
  getAllListings,
  getListingById,
  searchListings
} from "../controllers/listing.controller.js";

const router = express.Router();

router.get("/", getAllListings);
router.get("/search", searchListings);
router.get("/:id", getListingById);

export default router;