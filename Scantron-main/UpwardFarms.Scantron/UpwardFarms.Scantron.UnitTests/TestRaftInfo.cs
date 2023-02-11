using System;
using Xunit;

namespace UnitTests
{
    public class TestRaftInfo
    {
        [Fact]
        public void FarmRaftInfo_should_ReportEmptyStatusWhenNotValid()
        {
            var raft = new UpwardFarms.Scantron.FarmRaftInfo();

            Assert.Equal("", raft.latestStatus());

            raft = new UpwardFarms.Scantron.FarmRaftInfo(false);

            Assert.Equal("", raft.latestStatus());
        }

        [Fact]
        public void FarmRaftInfo_should_ReportUnusedIfNoFieldsCompleted()
        {
            var raft = new UpwardFarms.Scantron.FarmRaftInfo(true);

            Assert.Equal("Unused", raft.latestStatus());
        }

        [Fact]
        public void FarmRaftInfo_should_ReportFutureSeeding()
        {
            var raft = new UpwardFarms.Scantron.FarmRaftInfo(true);

            raft.seedingDate = "2/4/2021";

            Assert.Equal("To Seed:", raft.seedingPrompt());
            Assert.Equal("To Transplant:", raft.transplantPrompt());
            Assert.Equal("To Harvest:", raft.harvestPrompt());
            Assert.Equal("To Seed: 2/4/2021", raft.latestStatus());
        }

        [Fact]
        public void FarmRaftInfo_should_ReportSeeding()
        {
            var raft = new UpwardFarms.Scantron.FarmRaftInfo(true);

            raft.seedingDate = "2/4/2021";
            raft.seederInitials = "BOB";

            Assert.Equal("Seeded:", raft.seedingPrompt());
            Assert.Equal("To Transplant:", raft.transplantPrompt());
            Assert.Equal("To Harvest:", raft.harvestPrompt());
            Assert.Equal("Seeded: 2/4/2021 BOB", raft.latestStatus());
        }

        [Fact]
        public void FarmRaftInfo_should_ReportFutureTransplanting()
        {
            var raft = new UpwardFarms.Scantron.FarmRaftInfo(true);

            raft.seedingDate = "2/4/2021";
            raft.seederInitials = "BOB";
            raft.transplantDate = "2/11/2021";

            Assert.Equal("Seeded:", raft.seedingPrompt());
            Assert.Equal("To Transplant:", raft.transplantPrompt());
            Assert.Equal("To Harvest:", raft.harvestPrompt());
            Assert.Equal("Seeded: 2/4/2021 BOB", raft.latestStatus());
        }

        [Fact]
        public void FarmRaftInfo_should_ReportTransplant()
        {
            var raft = new UpwardFarms.Scantron.FarmRaftInfo(true);

            raft.seedingDate = "2/4/2021";
            raft.seederInitials = "BOB";
            raft.transplantDate = "2/11/2021";
            raft.transplanterInitials = "EDY";

            Assert.Equal("Seeded:", raft.seedingPrompt());
            Assert.Equal("Transplanted:", raft.transplantPrompt());
            Assert.Equal("To Harvest:", raft.harvestPrompt());
            Assert.Equal("Transplanted: 2/11/2021 EDY", raft.latestStatus());
        }

        [Fact]
        public void FarmRaftInfo_should_ReportFutureHarvests()
        {
            var raft = new UpwardFarms.Scantron.FarmRaftInfo(true);

            raft.seedingDate = "2/4/2021";
            raft.seederInitials = "BOB";
            raft.transplantDate = "2/11/2021";
            raft.transplanterInitials = "EDY";
            raft.harvestDate = "2/18/2021";

            Assert.Equal("Seeded:", raft.seedingPrompt());
            Assert.Equal("Transplanted:", raft.transplantPrompt());
            Assert.Equal("To Harvest:", raft.harvestPrompt());
            Assert.Equal("Transplanted: 2/11/2021 EDY", raft.latestStatus());
        }

        [Fact]
        public void FarmRaftInfo_should_ReportHarvests()
        {
            var raft = new UpwardFarms.Scantron.FarmRaftInfo(true);

            raft.seedingDate = "2/4/2021";
            raft.seederInitials = "BOB";
            raft.transplantDate = "2/11/2021";
            raft.transplanterInitials = "EDY";
            raft.harvestDate = "2/18/2021";
            raft.harvesterInitials = "ANN";

            Assert.Equal("Seeded:", raft.seedingPrompt());
            Assert.Equal("Transplanted:", raft.transplantPrompt());
            Assert.Equal("Harvested:", raft.harvestPrompt());
            Assert.Equal("Harvested: 2/18/2021 ANN", raft.latestStatus());
        }

        [Fact]
        public void FarmRaftInfo_should_NotCareAboutMissingIntermediateSteps()
        {
            var raft = new UpwardFarms.Scantron.FarmRaftInfo(true);

            raft.seedingDate = "2/4/2021";
            raft.seederInitials = "BOB";
            raft.transplantDate = null;
            raft.transplanterInitials = null;
            raft.harvestDate = "2/18/2021";
            raft.harvesterInitials = "ANN";

            Assert.Equal("Seeded:", raft.seedingPrompt());
            Assert.Equal("To Transplant:", raft.transplantPrompt());
            Assert.Equal("Harvested:", raft.harvestPrompt());
            Assert.Equal("Harvested: 2/18/2021 ANN", raft.latestStatus());
        }

        [Fact]
        public void FarmRaftInfo_should_NotCareAboutMissingDates()
        {
            var raft = new UpwardFarms.Scantron.FarmRaftInfo(true);

            raft.seedingDate = null;
            raft.seederInitials = "BOB";
            raft.transplantDate = "2/11/2021";
            raft.transplanterInitials = "EDY";
            raft.harvestDate = null;
            raft.harvesterInitials = "ANN";

            Assert.Equal("Seeded:", raft.seedingPrompt());
            Assert.Equal("Transplanted:", raft.transplantPrompt());
            Assert.Equal("Harvested:", raft.harvestPrompt());
            Assert.Equal("Harvested:  ANN", raft.latestStatus());
        }
    }
}
