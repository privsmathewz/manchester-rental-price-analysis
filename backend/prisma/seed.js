// backend/prisma/seed.js
import { PrismaClient } from "@prisma/client";

const prisma = new PrismaClient();

async function main() {
  console.log("Seeding database...");

  await prisma.rentalListing.deleteMany();
  await prisma.source.deleteMany();

  const source1 = await prisma.source.create({
    data: {
      title: "Manchester Rental Market Outlook 2026",
      sourceName: "Knight Knox",
      url: "https://example.com/knight-knox-manchester-rental-market-2026",
      publishedDate: new Date("2025-08-15"),
      accessedDate: new Date("2026-03-10"),
      summary:
        "Reported Manchester average monthly rent at around £1,317 in August 2025 and highlighted strong yields in popular rental districts."
    }
  });

  const source2 = await prisma.source.create({
    data: {
      title: "Manchester Property Yield Analysis",
      sourceName: "Joseph Mews",
      url: "https://example.com/joseph-mews-manchester-yields",
      publishedDate: new Date("2025-11-20"),
      accessedDate: new Date("2026-03-10"),
      summary:
        "Discussed postcode-level rental yields in Manchester, including strong student demand in M14 and other high-performing areas."
    }
  });

  const source3 = await prisma.source.create({
    data: {
      title: "Manchester Student Housing Demand Update",
      sourceName: "UCAS / Market Summary",
      url: "https://example.com/manchester-student-housing-demand",
      publishedDate: new Date("2025-09-01"),
      accessedDate: new Date("2026-03-10"),
      summary:
        "Summarised continued student demand and its impact on rental pressure in university-adjacent postcodes."
    }
  });

  const listings = [
    {
      postcode: "M1",
      propertyType: "Studio",
      avgRent: 909.93,
      avgPrice: 149793.0,
      yieldPercent: 7.29,
      propertySizeSqft: 356,
      distanceToCityCenterKm: 3.62,
      distanceToUniversityKm: 1.91,
      date: "2025-01",
      sourceId: source1.id
    },
    {
      postcode: "M1",
      propertyType: "1-bed",
      avgRent: 1181.66,
      avgPrice: 199814.0,
      yieldPercent: 7.10,
      propertySizeSqft: 908,
      distanceToCityCenterKm: 3.96,
      distanceToUniversityKm: 1.92,
      date: "2025-01",
      sourceId: source1.id
    },
    {
      postcode: "M1",
      propertyType: "HMO",
      avgRent: 1488.38,
      avgPrice: 249212.0,
      yieldPercent: 7.17,
      propertySizeSqft: 1176,
      distanceToCityCenterKm: 2.97,
      distanceToUniversityKm: 1.95,
      date: "2025-01",
      sourceId: source1.id
    },
    {
      postcode: "M3",
      propertyType: "Studio",
      avgRent: 801.22,
      avgPrice: 140905.0,
      yieldPercent: 6.82,
      propertySizeSqft: 725,
      distanceToCityCenterKm: 4.40,
      distanceToUniversityKm: 0.93,
      date: "2025-01",
      sourceId: source2.id
    },
    {
      postcode: "M3",
      propertyType: "1-bed",
      avgRent: 1154.44,
      avgPrice: 188848.0,
      yieldPercent: 7.34,
      propertySizeSqft: 693,
      distanceToCityCenterKm: 2.87,
      distanceToUniversityKm: 0.43,
      date: "2025-01",
      sourceId: source2.id
    },
    {
      postcode: "M14",
      propertyType: "Studio",
      avgRent: 659.47,
      avgPrice: 121679.0,
      yieldPercent: 6.50,
      propertySizeSqft: 595,
      distanceToCityCenterKm: 2.39,
      distanceToUniversityKm: 2.15,
      date: "2025-01",
      sourceId: source3.id
    },
    {
      postcode: "M14",
      propertyType: "1-bed",
      avgRent: 929.57,
      avgPrice: 159757.0,
      yieldPercent: 6.98,
      propertySizeSqft: 958,
      distanceToCityCenterKm: 5.33,
      distanceToUniversityKm: 0.77,
      date: "2025-01",
      sourceId: source3.id
    },
    {
      postcode: "M14",
      propertyType: "HMO",
      avgRent: 1076.14,
      avgPrice: 199386.0,
      yieldPercent: 6.48,
      propertySizeSqft: 1287,
      distanceToCityCenterKm: 3.25,
      distanceToUniversityKm: 1.70,
      date: "2025-01",
      sourceId: source3.id
    },
    {
      postcode: "M5",
      propertyType: "Studio",
      avgRent: 723.44,
      avgPrice: 125295.0,
      yieldPercent: 6.93,
      propertySizeSqft: 651,
      distanceToCityCenterKm: 5.10,
      distanceToUniversityKm: 2.84,
      date: "2025-01",
      sourceId: source2.id
    },
    {
      postcode: "M13",
      propertyType: "Studio",
      avgRent: 681.93,
      avgPrice: 115629.0,
      yieldPercent: 7.08,
      propertySizeSqft: 742,
      distanceToCityCenterKm: 2.56,
      distanceToUniversityKm: 2.47,
      date: "2025-01",
      sourceId: source3.id
    },
    {
      postcode: "M1",
      propertyType: "Studio",
      avgRent: 929.74,
      avgPrice: 154786.0,
      yieldPercent: 7.21,
      propertySizeSqft: 393,
      distanceToCityCenterKm: 3.84,
      distanceToUniversityKm: 1.17,
      date: "2025-07",
      sourceId: source1.id
    },
    {
      postcode: "M3",
      propertyType: "1-bed",
      avgRent: 1160.49,
      avgPrice: 191116.0,
      yieldPercent: 7.29,
      propertySizeSqft: 451,
      distanceToCityCenterKm: 4.49,
      distanceToUniversityKm: 2.91,
      date: "2025-07",
      sourceId: source2.id
    },
    {
      postcode: "M14",
      propertyType: "1-bed",
      avgRent: 973.53,
      avgPrice: 162871.0,
      yieldPercent: 7.17,
      propertySizeSqft: 676,
      distanceToCityCenterKm: 3.49,
      distanceToUniversityKm: 2.84,
      date: "2025-07",
      sourceId: source3.id
    },
    {
      postcode: "M5",
      propertyType: "1-bed",
      avgRent: 1037.34,
      avgPrice: 168088.0,
      yieldPercent: 7.41,
      propertySizeSqft: 482,
      distanceToCityCenterKm: 4.17,
      distanceToUniversityKm: 1.67,
      date: "2025-07",
      sourceId: source2.id
    },
    {
      postcode: "M13",
      propertyType: "1-bed",
      avgRent: 969.69,
      avgPrice: 152590.0,
      yieldPercent: 7.63,
      propertySizeSqft: 696,
      distanceToCityCenterKm: 2.19,
      distanceToUniversityKm: 1.83,
      date: "2025-10",
      sourceId: source3.id
    }
  ];

  await prisma.rentalListing.createMany({
    data: listings
  });

  console.log("Seeding complete.");
}

main()
  .catch((error) => {
    console.error("Seed error:", error);
    process.exit(1);
  })
  .finally(async () => {
    await prisma.$disconnect();
  });