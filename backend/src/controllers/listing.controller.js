// backend/src/controllers/listing.controller.js
import prisma from "../config/db.js";

export const getAllListings = async (req, res) => {
  try {
    const listings = await prisma.rentalListing.findMany({
      include: {
        source: true
      },
      orderBy: [
        { date: "asc" },
        { postcode: "asc" }
      ]
    });

    res.status(200).json({
      success: true,
      count: listings.length,
      data: listings
    });
  } catch (error) {
    console.error("Error fetching listings:", error);
    res.status(500).json({
      success: false,
      message: "Failed to fetch rental listings"
    });
  }
};

export const getListingById = async (req, res) => {
  try {
    const id = Number(req.params.id);

    if (Number.isNaN(id)) {
      return res.status(400).json({
        success: false,
        message: "Invalid listing ID"
      });
    }

    const listing = await prisma.rentalListing.findUnique({
      where: { id },
      include: {
        source: true
      }
    });

    if (!listing) {
      return res.status(404).json({
        success: false,
        message: "Rental listing not found"
      });
    }

    res.status(200).json({
      success: true,
      data: listing
    });
  } catch (error) {
    console.error("Error fetching listing by ID:", error);
    res.status(500).json({
      success: false,
      message: "Failed to fetch rental listing"
    });
  }
};

export const searchListings = async (req, res) => {
  try {
    const { postcode, property_type, start_date, end_date } = req.query;

    const where = {};

    if (postcode) {
      where.postcode = {
        equals: postcode,
        mode: "insensitive"
      };
    }

    if (property_type) {
      where.propertyType = {
        equals: property_type,
        mode: "insensitive"
      };
    }

    if (start_date || end_date) {
      where.date = {};
      if (start_date) where.date.gte = start_date;
      if (end_date) where.date.lte = end_date;
    }

    const listings = await prisma.rentalListing.findMany({
      where,
      include: {
        source: true
      },
      orderBy: [
        { date: "asc" },
        { postcode: "asc" }
      ]
    });

    res.status(200).json({
      success: true,
      filters: {
        postcode: postcode || null,
        property_type: property_type || null,
        start_date: start_date || null,
        end_date: end_date || null
      },
      count: listings.length,
      data: listings
    });
  } catch (error) {
    console.error("Error searching listings:", error);
    res.status(500).json({
      success: false,
      message: "Failed to search rental listings"
    });
  }
};