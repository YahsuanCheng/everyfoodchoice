from flask import Flask, request, render_template, redirect, url_for, flash
import pandas as pd

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False  # 确保 JSON 响应使用 UTF-8 编码
app.secret_key = 'supersecretkey'  # 用于闪现消息

# 使用pandas读取Excel文件
df = pd.read_excel('foods.xlsx', engine='openpyxl')

# 确保数值列是数字类型
df['每份供應量熱量(大卡)'] = pd.to_numeric(df['每份供應量熱量(大卡)'], errors='coerce')
df['每份供應量重量(公克)'] = pd.to_numeric(df['每份供應量重量(公克)'], errors='coerce')
df['蛋白質(公克)'] = pd.to_numeric(df['蛋白質(公克)'], errors='coerce')
df['脂肪(公克)'] = pd.to_numeric(df['脂肪(公克)'], errors='coerce')
df['碳水化合物(公克)'] = pd.to_numeric(df['碳水化合物(公克)'], errors='coerce')

# 确保脂肪占热量比是字符串类型
df['脂肪佔熱量比(%)'] = df['脂肪佔熱量比(%)'].astype(str)

def recommend_foods(calorie_limit):
    # 选择热量在 calorie_limit 的食物范围
    min_calorie = calorie_limit - 200
    max_calorie = calorie_limit
    recommended = df[(df['每份供應量熱量(大卡)'] >= min_calorie) & (df['每份供應量熱量(大卡)'] <= max_calorie)]
    
    if len(recommended) > 3:
        sample = recommended.sample(n=3)
        sample = sample.sort_values(by='每份供應量熱量(大卡)')
    else:
        sample = recommended.sort_values(by='每份供應量熱量(大卡)')
    
    return sample



@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        calorie_limit = int(request.form['calorie_limit'])
        recommended = recommend_foods(calorie_limit)
        foods = recommended.to_dict('records')
        if not foods:
            flash('沒有符合你熱量上限的食物。', 'danger')
        return render_template('index.html', foods=foods)
    return render_template('index.html', foods=[])

@app.route('/reset', methods=['POST'])
def reset():
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
