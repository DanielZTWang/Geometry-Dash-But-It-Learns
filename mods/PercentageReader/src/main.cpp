#include <Geode/Geode.hpp>
#include <Geode/modify/PlayLayer.hpp>

#include <fstream>
#include <filesystem>
#include <string>

using namespace geode::prelude;

static std::filesystem::path getOutputPath() {
    auto dir = std::filesystem::path(
        "C:/Users/pakou/OneDrive/Documents/GitHub/Geometry-Dash-But-It-Learns" // REPLACE WITH OUTPUT PATH
    );

    std::filesystem::create_directories(dir);
    return dir / "gd_data.txt";
}

static void writeState(std::string percent, bool dead, bool completed) {
    std::ofstream file(getOutputPath(), std::ios::trunc);

    if (!file.is_open()) {
        return;
    }

    file << percent << ","
         << (dead ? "dead" : "alive") << ","
         << (completed ? "complete" : "incomplete");
}

class $modify(MyPlayLayer, PlayLayer) {
    bool init(GJGameLevel* level, bool useReplay, bool dontCreateObjects) {
        if (!PlayLayer::init(level, useReplay, dontCreateObjects)) {
            return false;
        }

        writeState("0.0", false, false);
        return true;
    }

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

    void destroyPlayer(PlayerObject* player, GameObject* object) {
        writeState("0.0", true, false);
        PlayLayer::destroyPlayer(player, object);
    }

    void resetLevel() {
        PlayLayer::resetLevel();
        writeState("0.0", false, false);
    }
};