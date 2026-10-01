import os
from PIL import Image, ImageFilter, ImageDraw

def blur_region(img, box, radius=12):
    # box is (left, upper, right, lower)
    cropped = img.crop(box)
    blurred = cropped.filter(ImageFilter.GaussianBlur(radius))
    img.paste(blurred, box)
    draw = ImageDraw.Draw(img)
    draw.rectangle(box, outline=(180, 180, 180), width=1)
    return img

os.makedirs("docs", exist_ok=True)

# 1. ECR Screenshot
ecr_path = '/Users/sithumuthsara/.gemini/antigravity-ide/brain/26a1b6a3-e9d3-4b36-b972-0a8f050b161b/.user_uploaded/media_1790871498923.png'
img_ecr = Image.open(ecr_path)
# Top-right account bar: x in [900, 1024], y in [0, 25]
img_ecr = blur_region(img_ecr, (900, 0, 1024, 25), radius=14)
# URI Account ID 122773994215: x in [325, 405], y in [96, 118]
img_ecr = blur_region(img_ecr, (325, 96, 405, 118), radius=14)
img_ecr.save("docs/aws_ecr_console.png")

# 2. EKS Cluster Screenshot
eks_path = '/Users/sithumuthsara/.gemini/antigravity-ide/brain/26a1b6a3-e9d3-4b36-b972-0a8f050b161b/.user_uploaded/media_1790871534234.png'
img_eks = Image.open(eks_path)
img_eks = blur_region(img_eks, (900, 0, 1024, 25), radius=14)
img_eks.save("docs/aws_eks_console.png")

# 3. IAM User Screenshot
iam_path = '/Users/sithumuthsara/.gemini/antigravity-ide/brain/26a1b6a3-e9d3-4b36-b972-0a8f050b161b/.user_uploaded/media_1790871573696.png'
img_iam = Image.open(iam_path)
img_iam = blur_region(img_iam, (900, 0, 1024, 25), radius=14)
# ARN account ID: x in [825, 892], y in [112, 126]
img_iam = blur_region(img_iam, (825, 112, 892, 126), radius=14)
img_iam.save("docs/aws_iam_console.png")

# 4. API Docs Overview Screenshot
api_overview_path = '/Users/sithumuthsara/.gemini/antigravity-ide/brain/26a1b6a3-e9d3-4b36-b972-0a8f050b161b/.user_uploaded/media_1790871614728.png'
img_api1 = Image.open(api_overview_path)
img_api1.save("docs/api_docs_overview.png")

# 5. API Docs Live Execution Screenshot
api_exec_path = '/Users/sithumuthsara/.gemini/antigravity-ide/brain/26a1b6a3-e9d3-4b36-b972-0a8f050b161b/.user_uploaded/media_1790871664575.png'
img_api2 = Image.open(api_exec_path)
img_api2.save("docs/api_docs_execution.png")

print("Re-processed all 5 screenshots successfully with perfect text alignment")
