// backend/src/app.js
import express from "express";
import cors from "cors";
import listingRoutes from "./routes/listing.routes.js";
import sourceRoutes from "./routes/source.routes.js";

const app = express();

app.use(cors());
app.use(express.json());

app.get("/", (req, res) => {
  res.status(200).json({
    success: true,
    message: "Manchester Rental Analysis API is running"
  });
});

app.use("/api/listings", listingRoutes);
app.use("/api/sources", sourceRoutes);

app.use((req, res) => {
  res.status(404).json({
    success: false,
    message: "Route not found"
  });
});

export default app;