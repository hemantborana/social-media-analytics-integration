# Social Media Analytics - Dataset Creation Script

import pandas as pd
import json
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import random
import numpy as np

print("Creating realistic social media datasets...\n")

# Set random seed for reproducibility
random.seed(42)
np.random.seed(42)

# ============================================================================
# DATASET 1: Social_Media_Posts.csv (Structured Data)
# ============================================================================
print("1. Creating Social_Media_Posts.csv...")

platforms = ['Facebook', 'Instagram', 'Twitter', 'LinkedIn']
post_types = ['Image', 'Video', 'Text', 'Link', 'Poll']
categories = ['Technology', 'Lifestyle', 'Business', 'Entertainment', 'Education']

# generate 150 posts over last 60 days
num_posts = 150
posts_data = []

base_date = datetime(2024, 10, 1)

for i in range(num_posts):
    post_id = f"POST_{1001 + i}"
    platform = random.choice(platforms)
    post_type = random.choice(post_types)
    category = random.choice(categories)
    
    # random date in last 60 days
    days_ago = random.randint(0, 59)
    post_date = base_date + timedelta(days=days_ago)
    post_timestamp = post_date.strftime('%Y-%m-%d %H:%M:%S')
    
    # realistic engagement numbers based on platform
    if platform == 'Instagram':
        likes = random.randint(50, 5000)
        shares = random.randint(10, 500)
    elif platform == 'Facebook':
        likes = random.randint(30, 3000)
        shares = random.randint(20, 800)
    elif platform == 'Twitter':
        likes = random.randint(20, 2000)
        shares = random.randint(50, 1000)  # retweets
    else:  # LinkedIn
        likes = random.randint(15, 1500)
        shares = random.randint(5, 300)
    
    comments = random.randint(5, 200)
    
    # some missing values to make it realistic
    if random.random() < 0.05:  # 5% missing category
        category = None
    if random.random() < 0.03:  # 3% missing shares
        shares = None
    
    posts_data.append({
        'post_id': post_id,
        'platform': platform,
        'post_type': post_type,
        'category': category,
        'post_date': post_timestamp,
        'likes': likes,
        'shares': shares,
        'comments': comments,
        'reach': likes * random.randint(3, 8)  # estimated reach
    })

posts_df = pd.DataFrame(posts_data)
posts_df.to_csv('data/raw/Social_Media_Posts.csv', index=False)
print(f"    Created {len(posts_df)} posts")
print(f"    Platforms: {posts_df['platform'].unique()}")
print(f"    Saved to: data/raw/Social_Media_Posts.csv\n")

# ============================================================================
# DATASET 2: User_Engagement.json (Semi-Structured Data)
# ============================================================================
print("2. Creating User_Engagement.json...")

# create engagement data for users across different posts
engagement_data = {
    "metadata": {
        "collection_date": "2024-12-11",
        "version": "1.0",
        "total_users": 500
    },
    "user_engagement": []
}

user_ids = [f"USER_{2001 + i}" for i in range(100)]  # 100 active users

for user_id in user_ids:
    # each user engages with 3-8 posts
    num_engagements = random.randint(3, 8)
    engaged_posts = random.sample(posts_data, num_engagements)
    
    user_record = {
        "user_id": user_id,
        "join_date": (datetime(2023, 1, 1) + timedelta(days=random.randint(0, 600))).strftime('%Y-%m-%d'),
        "engagement_history": []
    }
    
    for post in engaged_posts:
        engagement_type = random.choice(['like', 'comment', 'share', 'like_comment'])
        
        engagement = {
            "post_id": post['post_id'],
            "platform": post['platform'],
            "engagement_type": engagement_type,
            "timestamp": (datetime.strptime(post['post_date'], '%Y-%m-%d %H:%M:%S') + 
                         timedelta(hours=random.randint(1, 48))).strftime('%Y-%m-%d %H:%M:%S'),
            "time_spent_seconds": random.randint(5, 300) if engagement_type in ['like_comment', 'comment'] else random.randint(2, 30)
        }
        
        # sometimes add sentiment for comments
        if engagement_type in ['comment', 'like_comment']:
            engagement['sentiment'] = random.choice(['positive', 'neutral', 'negative'])
        
        user_record["engagement_history"].append(engagement)
    
    # add user metrics
    user_record["total_engagements"] = len(user_record["engagement_history"])
    user_record["favorite_platform"] = max(set([e['platform'] for e in user_record["engagement_history"]]), 
                                           key=[e['platform'] for e in user_record["engagement_history"]].count)
    
    engagement_data["user_engagement"].append(user_record)

# save as JSON
with open('data/raw/User_Engagement.json', 'w') as f:
    json.dump(engagement_data, f, indent=2)

print(f"    Created engagement data for {len(engagement_data['user_engagement'])} users")
print(f"    Total engagement records: {sum([len(u['engagement_history']) for u in engagement_data['user_engagement']])}")
print(f"    Saved to: data/raw/User_Engagement.json\n")

# ============================================================================
# DATASET 3: Platform_Metrics.xml (Semi-Structured Data)
# ============================================================================
print("3. Creating Platform_Metrics.xml...")

# create XML structure
root = ET.Element('social_media_metrics')
root.set('generated_date', '2024-12-11')
root.set('reporting_period', '60_days')

# add platform-specific metrics
for platform in platforms:
    platform_elem = ET.SubElement(root, 'platform')
    platform_elem.set('name', platform)
    
    # overall stats
    stats = ET.SubElement(platform_elem, 'statistics')
    
    total_posts = len([p for p in posts_data if p['platform'] == platform])
    ET.SubElement(stats, 'total_posts').text = str(total_posts)
    ET.SubElement(stats, 'total_followers').text = str(random.randint(5000, 50000))
    ET.SubElement(stats, 'avg_engagement_rate').text = str(round(random.uniform(2.5, 8.5), 2))
    ET.SubElement(stats, 'total_impressions').text = str(random.randint(100000, 1000000))
    
    # performance metrics
    performance = ET.SubElement(platform_elem, 'performance')
    ET.SubElement(performance, 'best_posting_time').text = random.choice(['09:00', '12:00', '15:00', '18:00', '21:00'])
    ET.SubElement(performance, 'avg_reach').text = str(random.randint(1000, 10000))
    ET.SubElement(performance, 'conversion_rate').text = str(round(random.uniform(1.0, 5.0), 2))
    
    # demographics
    demographics = ET.SubElement(platform_elem, 'demographics')
    ET.SubElement(demographics, 'primary_age_group').text = random.choice(['18-24', '25-34', '35-44', '45-54'])
    ET.SubElement(demographics, 'gender_split').text = f"{random.randint(40, 60)}% Male, {random.randint(40, 60)}% Female"
    ET.SubElement(demographics, 'top_location').text = random.choice(['United States', 'India', 'United Kingdom', 'Canada'])
    
    # weekly breakdown
    weekly = ET.SubElement(platform_elem, 'weekly_metrics')
    for week in range(1, 9):  # 8 weeks
        week_elem = ET.SubElement(weekly, 'week')
        week_elem.set('number', str(week))
        ET.SubElement(week_elem, 'posts').text = str(random.randint(3, 12))
        ET.SubElement(week_elem, 'engagement').text = str(random.randint(500, 5000))
        ET.SubElement(week_elem, 'reach').text = str(random.randint(2000, 20000))

# create pretty XML with indentation
def indent_xml(elem, level=0):
    i = "\n" + level * "  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for child in elem:
            indent_xml(child, level + 1)
        if not child.tail or not child.tail.strip():
            child.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

indent_xml(root)

# save XML
tree = ET.ElementTree(root)
tree.write('data/raw/Platform_Metrics.xml', encoding='utf-8', xml_declaration=True)

print(f"    Created metrics for {len(platforms)} platforms")
print(f"    Includes: statistics, performance, demographics, weekly trends")
print(f"    Saved to: data/raw/Platform_Metrics.xml\n")

print("="*60)
print(" ALL DATASETS CREATED SUCCESSFULLY!")
print("="*60)
print("\nDataset Summary:")
print(f"  • CSV: {len(posts_df)} social media posts")
print(f"  • JSON: {len(engagement_data['user_engagement'])} users with engagement history")
print(f"  • XML: {len(platforms)} platforms with detailed metrics")
