// backend/src/controllers/source.controller.js
import prisma from "../config/db.js";

export const getAllSources = async (req, res) => {
  try {
    const sources = await prisma.source.findMany({
      orderBy: {
        id: "asc"
      }
    });

    res.status(200).json({
      success: true,
      count: sources.length,
      data: sources
    });
  } catch (error) {
    console.error("Error fetching sources:", error);
    res.status(500).json({
      success: false,
      message: "Failed to fetch sources"
    });
  }
};

export const getSourceById = async (req, res) => {
  try {
    const id = Number(req.params.id);

    if (Number.isNaN(id)) {
      return res.status(400).json({
        success: false,
        message: "Invalid source ID"
      });
    }

    const source = await prisma.source.findUnique({
      where: { id },
      include: {
        rentalListings: {
          orderBy: {
            date: "asc"
          }
        }
      }
    });

    if (!source) {
      return res.status(404).json({
        success: false,
        message: "Source not found"
      });
    }

    res.status(200).json({
      success: true,
      data: source
    });
  } catch (error) {
    console.error("Error fetching source by ID:", error);
    res.status(500).json({
      success: false,
      message: "Failed to fetch source"
    });
  }
};