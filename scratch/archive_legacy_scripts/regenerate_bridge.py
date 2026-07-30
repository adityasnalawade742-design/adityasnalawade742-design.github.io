from modules.bridge_creator import generate_bridge_page

product_data = {
    'title': 'Fenmzee Cozy Bedside Touch Lamp for Bedroom',
    'price': '$19.99',
    'affiliate_url': 'https://www.amazon.com/dp/B0BZXNSW5K?tag=adityasnalawa-20',
    'images': ['./output/images/raw_amazon_B0BZXNSW5K_0.jpg']
}

seo_data = {
    'pin_title': 'Cozy Bedside Touch Lamp',
    'description': 'Transform your nightstand setup with this dimmable touch bedside lamp featuring built-in USB A+C charging ports and a warm ambient glow.'
}

generate_bridge_page(product_data, seo_data, 'B0BZXNSW5K')
print("Done re-generating luxury bridge page for B0BZXNSW5K!")
