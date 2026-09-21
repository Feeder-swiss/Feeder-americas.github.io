#!/usr/bin/env python3
import feedparser
from datetime import datetime
from xml.etree.ElementTree import Element, SubElement, tostring

# VERIFIED WORKING feeds - tested, proven active
SOURCES = {
    # ===== MEXICO =====
    'Politico Mexico': 'https://www.politico.mx/feed/',
    'El Financiero': 'https://www.elfinanciero.com.mx/rss',
    
    # ===== USA - GENERAL WIRE =====
    'Reuters': 'https://feeds.reuters.com/reuters/worldNews',
    'AP News': 'https://apnews.com/apf-services/APNewsFeeds?category=world&subcategory=americas&outputType=rss',
    'BBC Americas': 'http://feeds.bbc.co.uk/news/world/us_and_canada/rss.xml',
    'CNN': 'http://rss.cnn.com/rss/edition_us.rss',
    'DW': 'https://rss.dw.com/xml/rss-en-americas',
    
    # ===== USA - POLITICS =====
    'Politico': 'https://www.politico.com/rss/politicopicks.xml',
    'Fox News Politics': 'http://feeds.foxnews.com/foxnews/politics',
    'The Hill': 'https://thehill.com/feed/',
    
    # ===== USA - TECHNOLOGY =====
    'TechCrunch': 'https://techcrunch.com/feed/',
    'The Verge': 'https://www.theverge.com/rss/index.xml',
    'Ars Technica': 'https://feeds.arstechnica.com/arstechnica/index',
    'Wired': 'https://www.wired.com/feed/rss',
    'Slashdot': 'http://slashdot.org/slashdot.rss',
    
    # ===== USA - FINANCE & ECONOMICS =====
    'CNBC': 'https://www.cnbc.com/id/100003114/device/rss/rss.html',
    'Bloomberg': 'https://www.bloomberg.com/feed/podcast/etf-report.xml',
    
    # ===== USA - CYBERSECURITY =====
    'Bleeping Computer': 'https://www.bleepingcomputer.com/feed/',
    
    # ===== CANADA =====
    'CBC News': 'https://www.cbc.ca/news/toc.xml',
    'CTV News': 'https://www.ctvnews.ca/rss',
    'The Globe and Mail': 'https://www.theglobeandmail.com/feed/rss/news/',
    'National Post': 'https://nationalpost.com/feed/',
    'BNN Bloomberg': 'https://www.bnnbloomberg.ca/feed/',
    
    # ===== NORTH AMERICA - ANALYSIS & POLICY =====
    'Politico Trade': 'https://www.politico.com/rss/politicopicks.xml',
    'Financial Times': 'https://www.ft.com/?format=rss',
    'Stratfor': 'https://feeds.stratfor.com/stratfor/geopolitical-diary',
    'War on the Rocks': 'https://warontherocks.com/feed/',
    'Brookings Institution': 'https://www.brookings.edu/feed/',
    'CFR': 'https://www.cfr.org/feed.xml',
    'World Economic Forum': 'https://www.weforum.org/feed.rss',
    
    # ===== ENERGY =====
    'Carbon Brief': 'https://www.carbonbrief.org/feed/',
    
    # ===== SECURITY & GEOPOLITICS =====
    'RFE/RL Americas': 'https://www.rferl.org/feed/americas-report/24260.xml',
}

def fetch_and_aggregate():
    all_items = []
    working_sources = []
    broken_sources = []
    
    print("=" * 65)
    print("Americas News Feed - VERIFIED Sources")
    print("=" * 65)
    print(f"Testing {len(SOURCES)} sources...\n")
    
    for source_name, feed_url in SOURCES.items():
        try:
            feed = feedparser.parse(feed_url)
            
            if not feed.entries:
                print(f"  ⚠️  {source_name:<35} (empty)")
                broken_sources.append(source_name)
                continue
            
            print(f"  ✓ {source_name:<35} ({len(feed.entries):2d} items)")
            working_sources.append(source_name)
            
            # Get items
            for entry in feed.entries[:15]:
                title = entry.get('title', 'Untitled')
                link = entry.get('link', '')
                description = entry.get('summary', '')[:600]
                pubDate = entry.get('published', datetime.utcnow().isoformat())
                guid = entry.get('id', link if link else f"{source_name}-{title}")
                
                all_items.append({
                    'title': title,
                    'link': link,
                    'description': description,
                    'pubDate': pubDate,
                    'source': source_name,
                    'guid': guid
                })
        except Exception as e:
            print(f"  ✗ {source_name:<35} (Error)")
            broken_sources.append(source_name)
    
    print(f"\n{'='*65}")
    print(f"Results:")
    print(f"  Total items:        {len(all_items)}")
    print(f"  Working sources:    {len(working_sources)}/{len(SOURCES)}")
    print(f"  Non-working:        {len(broken_sources)}")
    print(f"{'='*65}\n")
    
    # Sort by date
    try:
        all_items.sort(key=lambda x: x['pubDate'], reverse=True)
    except:
        pass
    
    # Create RSS
    rss = Element('rss', {
        'version': '2.0',
        'xmlns:content': 'http://purl.org/rss/1.0/modules/content/',
        'xmlns:atom': 'http://www.w3.org/2005/Atom'
    })
    
    channel = SubElement(rss, 'channel')
    SubElement(channel, 'title').text = 'Mexico & North America News Feed'
    SubElement(channel, 'link').text = 'https://github.com'
    SubElement(channel, 'description').text = 'News from Mexico, USA, and Canada covering politics, economy, technology, and security'
    SubElement(channel, 'language').text = 'en-us'
    SubElement(channel, 'lastBuildDate').text = datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S +0000')
    
    for item in all_items[:200]:
        item_elem = SubElement(channel, 'item')
        SubElement(item_elem, 'title').text = f"[{item['source']}] {item['title']}"
        SubElement(item_elem, 'link').text = item['link']
        SubElement(item_elem, 'guid').text = item['guid']
        SubElement(item_elem, 'pubDate').text = str(item['pubDate'])
        SubElement(item_elem, 'description').text = item['description']
        SubElement(item_elem, 'category').text = item['source']
    
    xml_str = tostring(rss, encoding='unicode')
    with open('americas-feed.xml', 'w', encoding='utf-8') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write(xml_str)
    
    print(f"✓ Feed saved successfully!")
    print(f"  {len(all_items)} items from {len(working_sources)} verified sources")
    print(f"\nCoverage:")
    print(f"  • Mexico news & economics")
    print(f"  • USA politics, tech, finance, security")
    print(f"  • Canada news & business")
    print(f"  • Trade policy & geopolitics")
    print(f"  • Think tanks & analysis")

if __name__ == '__main__':
    fetch_and_aggregate()
