-- CreateEnum
CREATE TYPE "LogLevel" AS ENUM ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL');

-- CreateTable
CREATE TABLE "Services" (
    "service_id" SERIAL NOT NULL,
    "service_name" TEXT NOT NULL,
    "is_active" BOOLEAN NOT NULL DEFAULT true,

    CONSTRAINT "Services_pkey" PRIMARY KEY ("service_id")
);

-- CreateTable
CREATE TABLE "Log" (
    "log_id" SERIAL NOT NULL,
    "user_id" INTEGER NOT NULL,
    "log_level" "LogLevel" NOT NULL,
    "message" TEXT,
    "log_timestamp" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "service_id" INTEGER NOT NULL,

    CONSTRAINT "Log_pkey" PRIMARY KEY ("log_id")
);

-- CreateIndex
CREATE UNIQUE INDEX "Services_service_name_key" ON "Services"("service_name");

-- AddForeignKey
ALTER TABLE "Log" ADD CONSTRAINT "Log_service_id_fkey" FOREIGN KEY ("service_id") REFERENCES "Services"("service_id") ON DELETE RESTRICT ON UPDATE CASCADE;
