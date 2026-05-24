#include <Geode/Geode.hpp>
#include <Geode/modify/PlayLayer.hpp>

#include <fstream>
#include <filesystem>
#include <string>

using namespace geode::prelude;

static std::filesystem::path getOutputPath() {
	// Gets the output path for data
    auto dir = std::filesystem::path(
        "C:/Users/pakou/OneDrive/Documents/GitHub/Geometry-Dash-But-It-Learns" //REPLACE WITH OUTPUT PATH
    );

	// Create the directory if it doesn't exist and return the path to the output file
    std::filesystem::create_directories(dir);
    return dir / "gd_data.txt";
}

static void writeState(std::string percent, bool dead, bool completed) {
	// Get the output file
    std::ofstream file(getOutputPath(), std::ios::trunc);

	// Check if file exists
    if (!file.is_open()) {
        return;
    }

	// Write the current status to file
    file << percent << ","
         << (dead ? "dead" : "alive") << ","
         << (completed ? "complete" : "incomplete");
}

class $modify(MyPlayLayer, PlayLayer) {
	// Write starting game data to file
	bool init(GJGameLevel* level, bool useReplay, bool dontCreateObjects) {
        if (!PlayLayer::init(level, useReplay, dontCreateObjects)) {
            return false;
        }

        writeState("0.0", false, false);

        return true;
    }

	// Write data to file after each update
	void postUpdate(float dt) {
        PlayLayer::postUpdate(dt);

		std::string percent = "0.0";

		if (this->m_percentageLabel) {
			percent = this->m_percentageLabel->getString();

			if (!percent.empty() && percent.back() == '%') {
				percent.pop_back();
			}
		}

		bool completed = this->m_hasCompletedLevel;

		writeState(percent, false, completed);
    }

	// Update death status
    void destroyPlayer(PlayerObject* player, GameObject* object) {
        writeState("0.0", true, false);

        PlayLayer::destroyPlayer(player, object);
    }

	// Reset data state
    void resetLevel() {
        PlayLayer::resetLevel();

        writeState("0.0", false, false);
    }
};