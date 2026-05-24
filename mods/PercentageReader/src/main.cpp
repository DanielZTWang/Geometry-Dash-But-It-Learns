#include <Geode/Geode.hpp>
#include <Geode/modify/PlayLayer.hpp>

#include <fstream>
#include <filesystem>
#include <string>

using namespace geode::prelude;

static std::filesystem::path getOutputPath() {
    return Mod::get()->getSaveDir() / "gd_percent.txt";
}

static void writeState(float percent, bool dead, bool completed) {
    std::ofstream file(getOutputPath(), std::ios::trunc);

    if (!file.is_open()) {
        return;
    }

    file << percent << ","
         << (dead ? "dead" : "alive") << ","
         << (completed ? "complete" : "incomplete");
}

class $modify(MyPlayLayer, PlayLayer) {

	struct Fields {
		CCSprite* m_bgSprite;
	};

	bool init(GJGameLevel* p0, bool p1, bool p2) {
		if (!PlayLayer::init(p0, p1, p2)) {
			return false;
		}

		CCMenu* menu = CCMenu::create();

		m_fields->m_bgSprite = CCSprite::create("bg.png"_spr);
		m_fields->m_bgSprite->setAnchorPoint({0.0f, 1.0f});
		m_fields->m_bgSprite->setPosition(ccp(390, 320));
		m_fields->m_bgSprite->setVisible(true);

		this->addChild(m_fields->m_bgSprite);

		return true;
	}
};