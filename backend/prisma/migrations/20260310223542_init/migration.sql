-- CreateTable
CREATE TABLE "Source" (
    "id" SERIAL NOT NULL,
    "title" TEXT NOT NULL,
    "sourceName" TEXT NOT NULL,
    "url" TEXT NOT NULL,
    "publishedDate" TIMESTAMP(3),
    "accessedDate" TIMESTAMP(3) NOT NULL,
    "summary" TEXT NOT NULL,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "Source_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "RentalListing" (
    "id" SERIAL NOT NULL,
    "postcode" TEXT NOT NULL,
    "propertyType" TEXT NOT NULL,
    "avgRent" DOUBLE PRECISION NOT NULL,
    "avgPrice" DOUBLE PRECISION NOT NULL,
    "yieldPercent" DOUBLE PRECISION NOT NULL,
    "propertySizeSqft" INTEGER,
    "distanceToCityCenterKm" DOUBLE PRECISION,
    "distanceToUniversityKm" DOUBLE PRECISION,
    "date" TEXT NOT NULL,
    "sourceId" INTEGER NOT NULL,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "RentalListing_pkey" PRIMARY KEY ("id")
);

-- CreateIndex
CREATE UNIQUE INDEX "Source_url_key" ON "Source"("url");

-- CreateIndex
CREATE INDEX "RentalListing_postcode_idx" ON "RentalListing"("postcode");

-- CreateIndex
CREATE INDEX "RentalListing_propertyType_idx" ON "RentalListing"("propertyType");

-- CreateIndex
CREATE INDEX "RentalListing_date_idx" ON "RentalListing"("date");

-- CreateIndex
CREATE INDEX "RentalListing_sourceId_idx" ON "RentalListing"("sourceId");

-- AddForeignKey
ALTER TABLE "RentalListing" ADD CONSTRAINT "RentalListing_sourceId_fkey" FOREIGN KEY ("sourceId") REFERENCES "Source"("id") ON DELETE CASCADE ON UPDATE CASCADE;
