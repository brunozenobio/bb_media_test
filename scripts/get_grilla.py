from playwright.sync_api import sync_playwright
from init_pluto_tv import *



url_base = "https://pluto.tv"
page,browser,_ = init_playwright()
init_pluto(page,url_base)

page.wait_for_selector('//div[contains(@class,"channelList-0-2") and contains(@class,"custom-scroll")]')
div_scroll_channel = page.locator('//div[contains(@class,"channelList-0-2") and contains(@class,"custom-scroll")]')


div_secciones_channels = div_scroll_channel.locator('//div[@role="rowheader"]').all()




for div_channel in div_secciones_channels:
    url_channel = url_base + div_channel.locator("a.ChannelInfo-Link").get_attribute("href")
    nombre_channel = div_channel.locator("div.image")
    span_timeline = div_channel.locator("+ span")
    








browser.close()
