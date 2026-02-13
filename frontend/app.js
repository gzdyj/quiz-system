// 自动检测后端地址
// - 本地开发: 使用 http://localhost:5000
// - Replit: 使用同源 /api
// - 其他: 使用 /api
const API_BASE = (() => {
    const hostname = window.location.hostname;
    const port = window.location.port;
    
    // 本地开发环境（8000 端口）
    if (port === '8000' || (hostname === 'localhost' && port === '8000')) {
        return 'http://localhost:5000/api';
    }
    
    // Replit 和其他部署环境
    return '/api';
})();
let currentPage = 1;
let currentQuestion = null;
let userId = 'user_' + Date.now();

// 初始化
document.addEventListener('DOMContentLoaded', () => {
    const savedUserId = localStorage.getItem('userId');
    if (savedUserId) {
        userId = savedUserId;
        document.getElementById('userId').value = userId;
    }
    loadQuestions();
});

// 用户ID变更
document.getElementById('userId').addEventListener('change', (e) => {
    userId = e.target.value || 'user_' + Date.now();
    localStorage.setItem('userId', userId);
});

// 视图切换
function switchView(viewName) {
    document.querySelectorAll('.view').forEach(v => v.classList.remove('active'));
    document.getElementById(viewName + 'View').classList.add('active');
    
    document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
    event.target.classList.add('active');
    
    if (viewName === 'stats') {
        loadStats();
    }
}

// 加载题目列表
async function loadQuestions() {
    try {
        const difficulty = document.getElementById('difficultyFilter')?.value || '';
        const type = document.getElementById('typeFilter')?.value || '';
        
        let url = `${API_BASE}/questions?page=${currentPage}&per_page=5`;
        if (difficulty) url += `&difficulty=${difficulty}`;
        if (type) url += `&type=${type}`;
        
        const response = await fetch(url);
        const data = await response.json();
        
        renderQuestions(data.data);
        updatePagination(data);
    } catch (error) {
        console.error('加载题目失败:', error);
        alert('加载题目失败');
    }
}

// 渲染题目列表
function renderQuestions(questions) {
    const container = document.getElementById('questionsList');
    container.innerHTML = '';
    
    questions.forEach(q => {
        const difficultyClass = `badge-${q.difficulty}`;
        const typeClass = `badge-${q.questionType === 'single' ? 'single' : 'multiple'}`;
        const typeText = q.questionType === 'single' ? '单选题' : '多选题';
        const difficultyText = {
            easy: '简单',
            medium: '中等',
            hard: '困难'
        }[q.difficulty] || '未知';
        
        const card = document.createElement('div');
        card.className = 'question-card';
        card.innerHTML = `
            <div class="question-header">
                <div class="question-title">${q.title}</div>
                <div class="question-meta">
                    <span class="badge ${difficultyClass}">${difficultyText}</span>
                    <span class="badge ${typeClass}">${typeText}</span>
                </div>
            </div>
            <div class="question-description">${q.description || '暂无描述'}</div>
            <div class="question-actions">
                <button class="btn btn-primary" onclick="viewQuestion(${q.id})">查看详情</button>
            </div>
        `;
        container.appendChild(card);
    });
}

// 查看题目详情并答题
async function viewQuestion(questionId) {
    try {
        const response = await fetch(`${API_BASE}/questions/${questionId}`);
        const q = await response.json();
        currentQuestion = q;
        
        const detailDiv = document.getElementById('questionDetail');
        const typeText = q.questionType === 'single' ? '单选题' : '多选题';
        const difficultyText = {
            easy: '简单',
            medium: '中等',
            hard: '困难'
        }[q.difficulty];
        
        const inputType = q.questionType === 'single' ? 'radio' : 'checkbox';
        const groupName = 'options_' + q.id;
        
        let optionsHtml = '';
        q.options.forEach(opt => {
            optionsHtml += `
                <div class="option">
                    <input type="${inputType}" id="opt_${opt.id}" name="${groupName}" value="${opt.id}">
                    <label for="opt_${opt.id}">${opt.id}. ${opt.text}</label>
                </div>
            `;
        });
        
        detailDiv.innerHTML = `
            <div class="question-detail">
                <div class="question-detail-info">
                    <span class="badge badge-${q.difficulty}">${difficultyText}</span>
                    <span class="badge badge-${q.questionType}">${typeText}</span>
                </div>
                <h2>${q.title}</h2>
                <div class="question-description-detail">${q.description || '暂无描述'}</div>
                <div class="options-group">
                    ${optionsHtml}
                </div>
                <button class="submit-btn" onclick="submitAnswer()">提交答案</button>
            </div>
        `;
        
        switchView('answer');
    } catch (error) {
        console.error('加载题目详情失败:', error);
        alert('加载题目详情失败');
    }
}

// 提交答案
async function submitAnswer() {
    if (!currentQuestion) return;
    
    const inputType = currentQuestion.questionType === 'single' ? 'radio' : 'checkbox';
    const groupName = 'options_' + currentQuestion.id;
    const checkedInputs = document.querySelectorAll(`input[name="${groupName}"]:checked`);
    
    if (checkedInputs.length === 0) {
        alert('请选择答案');
        return;
    }
    
    const selectedAnswers = Array.from(checkedInputs).map(input => input.value);
    
    try {
        const response = await fetch(`${API_BASE}/answers`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                questionId: currentQuestion.id,
                userId: userId,
                selectedAnswers: selectedAnswers
            })
        });
        
        const result = await response.json();
        showResultModal(result);
    } catch (error) {
        console.error('提交答案失败:', error);
        alert('提交答案失败');
    }
}

// 显示答题结果模态框
function showResultModal(result) {
    const modal = document.getElementById('resultModal');
    const titleEl = document.getElementById('resultTitle');
    const bodyEl = document.getElementById('resultBody');
    
    if (result.isCorrect) {
        titleEl.innerHTML = '<span class="correct">✓ 回答正确！</span>';
        bodyEl.innerHTML = `<p>恭喜！您的答案正确。</p>`;
    } else {
        titleEl.innerHTML = '<span class="incorrect">✗ 回答错误</span>';
        bodyEl.innerHTML = `
            <p>您的答案：${result.selectedAnswers?.join(', ') || '未选择'}</p>
            <div class="correct-answer">
                <strong>正确答案：${result.correctAnswers.join(', ')}</strong>
            </div>
        `;
    }
    
    modal.classList.add('show');
}

// 关闭结果模态框
function closeResultModal() {
    document.getElementById('resultModal').classList.remove('show');
    backToList();
}

// 返回题目列表
function backToList() {
    currentPage = 1;
    switchView('questions');
    loadQuestions();
}

// 应用筛选
function applyFilters() {
    currentPage = 1;
    loadQuestions();
}

// 上一页
function previousPage() {
    if (currentPage > 1) {
        currentPage--;
        loadQuestions();
    }
}

// 下一页
function nextPage() {
    currentPage++;
    loadQuestions();
}

// 更新分页信息
function updatePagination(data) {
    const pageInfo = document.getElementById('pageInfo');
    pageInfo.textContent = `第 ${data.current} / ${data.pages} 页`;
    
    document.getElementById('prevBtn').disabled = currentPage === 1;
    document.getElementById('nextBtn').disabled = currentPage >= data.pages;
}

// 加载用户成绩统计
async function loadStats() {
    try {
        const response = await fetch(`${API_BASE}/stats/${userId}`);
        const stats = await response.json();
        renderStats(stats);
    } catch (error) {
        console.error('加载统计数据失败:', error);
        alert('加载统计数据失败');
    }
}

// 渲染统计信息
function renderStats(stats) {
    const container = document.getElementById('statsContent');
    
    container.innerHTML = `
        <div class="stats-input">
            <input type="text" id="statsUserId" placeholder="输入用户ID查看统计" value="${userId}">
            <button class="btn btn-primary" onclick="updateStatsUserId()">查询</button>
        </div>
        <div class="stats-grid">
            <div class="stat-card">
                <h4>总题数</h4>
                <div class="stat-value">${stats.total}</div>
            </div>
            <div class="stat-card success">
                <h4>正确数</h4>
                <div class="stat-value">${stats.correct}</div>
            </div>
            <div class="stat-card danger">
                <h4>错误数</h4>
                <div class="stat-value">${stats.incorrect}</div>
            </div>
            <div class="stat-card">
                <h4>正确率</h4>
                <div class="stat-value">${stats.accuracy}%</div>
            </div>
        </div>
    `;
}

// 更新统计用户ID
function updateStatsUserId() {
    const input = document.getElementById('statsUserId');
    userId = input.value || 'user_' + Date.now();
    loadStats();
}
