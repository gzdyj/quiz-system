/**
 * 管理后台前端应用
 */

// API 基础地址
const API_BASE = '/admin/api';
let authToken = null;
let currentUser = null;

// ==================== 初始化 ====================

document.addEventListener('DOMContentLoaded', () => {
    // 检查认证
    checkAuth();
    
    // 绑定事件
    bindNavigation();
    bindLogout();
    bindForms();
    
    // 加载初始数据
    loadDashboard();
});

function checkAuth() {
    authToken = localStorage.getItem('adminToken');
    if (!authToken) {
        showLoginForm();
        return false;
    }
    document.body.classList.add('authenticated');
    return true;
}

function showLoginForm() {
    document.body.innerHTML = `
        <div class="login-container">
            <div class="login-box">
                <h1>📚 管理后台</h1>
                <form id="loginForm">
                    <div class="form-group">
                        <input type="text" id="username" placeholder="用户名" class="input" required>
                    </div>
                    <div class="form-group">
                        <input type="password" id="password" placeholder="密码" class="input" required>
                    </div>
                    <button type="submit" class="btn btn-primary btn-block">登录</button>
                    <p class="hint">默认用户: admin / admin123</p>
                </form>
            </div>
        </div>
        <style>
            body { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
            .login-container { display: flex; align-items: center; justify-content: center; min-height: 100vh; }
            .login-box { background: white; padding: 40px; border-radius: 10px; box-shadow: 0 10px 40px rgba(0,0,0,0.2); width: 100%; max-width: 350px; }
            .login-box h1 { text-align: center; margin-bottom: 30px; color: var(--primary-color); }
            .btn-block { width: 100%; }
            .hint { text-align: center; font-size: 12px; color: #6c757d; margin-top: 15px; }
        </style>
    `;
    
    document.getElementById('loginForm').addEventListener('submit', handleLogin);
}

async function handleLogin(e) {
    e.preventDefault();
    
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    
    try {
        const response = await fetch(`${API_BASE}/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });
        
        if (response.ok) {
            const data = await response.json();
            authToken = data.token;
            currentUser = data.admin;
            localStorage.setItem('adminToken', authToken);
            location.reload();
        } else {
            alert('登录失败: ' + (await response.json()).error);
        }
    } catch (error) {
        alert('登录错误: ' + error.message);
    }
}

// ==================== 导航 ====================

function bindNavigation() {
    document.querySelectorAll('.nav-item').forEach(item => {
        item.addEventListener('click', (e) => {
            e.preventDefault();
            const section = item.dataset.section;
            
            // 更新活跃状态
            document.querySelectorAll('.nav-item').forEach(i => i.classList.remove('active'));
            item.classList.add('active');
            
            // 显示对应的部分
            document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
            document.getElementById(section).classList.add('active');
            
            // 更新标题
            const titles = {
                dashboard: '仪表板',
                questions: '题目管理',
                categories: '分类管理',
                users: '用户统计',
                profile: '账户设置'
            };
            document.getElementById('pageTitle').textContent = titles[section];
            
            // 加载数据
            switch (section) {
                case 'dashboard':
                    loadDashboard();
                    break;
                case 'questions':
                    loadQuestions();
                    break;
                case 'categories':
                    loadCategories();
                    break;
                case 'users':
                    loadUsers();
                    break;
                case 'profile':
                    loadProfile();
                    break;
            }
        });
    });
}

function bindLogout() {
    document.getElementById('logoutBtn').addEventListener('click', () => {
        localStorage.removeItem('adminToken');
        location.reload();
    });
}

function bindForms() {
    document.getElementById('addQuestionBtn')?.addEventListener('click', showAddQuestionForm);
    document.getElementById('addCategoryBtn')?.addEventListener('click', showAddCategoryForm);
    document.getElementById('changePasswordBtn')?.addEventListener('click', handleChangePassword);
}

// ==================== 仪表板 ====================

async function loadDashboard() {
    try {
        const response = await fetch(`${API_BASE}/statistics/overview`, {
            headers: { 'Authorization': `Bearer ${authToken}` }
        });
        
        if (response.ok) {
            const data = await response.json();
            document.getElementById('totalQuestions').textContent = data.totalQuestions;
            document.getElementById('publishedQuestions').textContent = data.publishedQuestions;
            document.getElementById('totalAnswers').textContent = data.totalAnswers;
            document.getElementById('totalUsers').textContent = data.totalUsers;
            document.getElementById('accuracy').textContent = data.accuracy + '%';
        }
    } catch (error) {
        console.error('加载仪表板失败:', error);
    }
}

// ==================== 题目管理 ====================

async function loadQuestions(page = 1) {
    const difficulty = document.getElementById('difficultyFilter')?.value || '';
    const category = document.getElementById('categoryFilter')?.value || '';
    const search = document.getElementById('questionSearch')?.value || '';
    
    try {
        let url = `${API_BASE}/questions?page=${page}&per_page=20`;
        if (difficulty) url += `&difficulty=${difficulty}`;
        if (category) url += `&category=${category}`;
        if (search) url += `&search=${search}`;
        
        const response = await fetch(url, {
            headers: { 'Authorization': `Bearer ${authToken}` }
        });
        
        if (response.ok) {
            const data = await response.json();
            renderQuestionsTable(data.data);
        }
    } catch (error) {
        console.error('加载题目失败:', error);
    }
}

function renderQuestionsTable(questions) {
    const tbody = document.getElementById('questionsTableBody');
    
    if (questions.length === 0) {
        tbody.innerHTML = '<tr><td colspan="7" class="text-center">暂无题目</td></tr>';
        return;
    }
    
    tbody.innerHTML = questions.map(q => `
        <tr>
            <td>#${q.id}</td>
            <td>${q.title}</td>
            <td><span class="badge badge-${q.difficulty}">${getDifficultyText(q.difficulty)}</span></td>
            <td>${q.category || '-'}</td>
            <td>${q.questionType === 'single' ? '单选' : '多选'}</td>
            <td>${q.viewCount}</td>
            <td>
                <button class="btn btn-sm" onclick="editQuestion(${q.id})">编辑</button>
                <button class="btn btn-sm btn-danger" onclick="deleteQuestion(${q.id})">删除</button>
            </td>
        </tr>
    `).join('');
}

function getDifficultyText(difficulty) {
    return { easy: '简单', medium: '中等', hard: '困难' }[difficulty] || difficulty;
}

async function editQuestion(id) {
    try {
        const response = await fetch(`${API_BASE}/questions/${id}`, {
            headers: { 'Authorization': `Bearer ${authToken}` }
        });
        
        if (response.ok) {
            const question = await response.json();
            showQuestionForm(question);
        }
    } catch (error) {
        console.error('加载题目失败:', error);
    }
}

async function deleteQuestion(id) {
    if (!confirm('确定要删除这道题目吗？')) return;
    
    try {
        await fetch(`${API_BASE}/questions/${id}`, {
            method: 'DELETE',
            headers: { 'Authorization': `Bearer ${authToken}` }
        });
        loadQuestions();
    } catch (error) {
        console.error('删除题目失败:', error);
    }
}

function showAddQuestionForm() {
    showQuestionForm(null);
}

function showQuestionForm(question) {
    const modal = document.getElementById('modal');
    const isEdit = !!question;
    
    const optionsHtml = question ? question.options.map((opt, i) => `
        <div class="form-group">
            <label>选项 ${String.fromCharCode(65 + i)}</label>
            <input type="text" value="${opt.text}" class="input option-text" data-id="${opt.id}">
        </div>
    `).join('') : '';
    
    const correctAnswers = question ? question.correctAnswers.join(', ') : '';
    
    document.getElementById('modalTitle').textContent = isEdit ? '编辑题目' : '添加题目';
    document.getElementById('modalBody').innerHTML = `
        <form id="questionForm">
            <div class="form-group">
                <label>题目标题</label>
                <input type="text" id="questionTitle" value="${question?.title || ''}" class="input" required>
            </div>
            <div class="form-group">
                <label>题目描述</label>
                <textarea id="questionDescription" class="input">${question?.description || ''}</textarea>
            </div>
            <div class="form-group">
                <label>题型</label>
                <select id="questionType" class="input">
                    <option value="single" ${question?.questionType === 'single' ? 'selected' : ''}>单选</option>
                    <option value="multiple" ${question?.questionType === 'multiple' ? 'selected' : ''}>多选</option>
                </select>
            </div>
            <div class="form-group">
                <label>难度</label>
                <select id="questionDifficulty" class="input">
                    <option value="easy" ${question?.difficulty === 'easy' ? 'selected' : ''}>简单</option>
                    <option value="medium" ${question?.difficulty === 'medium' ? 'selected' : ''}>中等</option>
                    <option value="hard" ${question?.difficulty === 'hard' ? 'selected' : ''}>困难</option>
                </select>
            </div>
            <div class="form-group">
                <label>分类</label>
                <input type="text" id="questionCategory" value="${question?.category || ''}" class="input">
            </div>
            <div class="form-group">
                <label>选项</label>
                ${optionsHtml || '<p class="text-center">加载中...</p>'}
            </div>
            <div class="form-group">
                <label>正确答案(逗号分隔)</label>
                <input type="text" id="correctAnswers" value="${correctAnswers}" class="input" placeholder="A,B" required>
            </div>
            <div class="form-group">
                <label>解析说明</label>
                <textarea id="questionExplanation" class="input">${question?.explanation || ''}</textarea>
            </div>
            <div style="text-align: right;">
                <button type="button" class="btn" onclick="closeModal()">取消</button>
                <button type="submit" class="btn btn-primary">${isEdit ? '更新' : '创建'}</button>
            </div>
        </form>
    `;
    
    modal.classList.add('show');
    
    document.getElementById('questionForm').addEventListener('submit', (e) => {
        e.preventDefault();
        handleSaveQuestion(question?.id);
    });
}

async function handleSaveQuestion(id) {
    const options = Array.from(document.querySelectorAll('.option-text')).map(el => ({
        id: el.dataset.id,
        text: el.value
    }));
    
    const data = {
        title: document.getElementById('questionTitle').value,
        description: document.getElementById('questionDescription').value,
        question_type: document.getElementById('questionType').value,
        options: options,
        correct_answers: document.getElementById('correctAnswers').value.split(',').map(s => s.trim()),
        difficulty: document.getElementById('questionDifficulty').value,
        category: document.getElementById('questionCategory').value,
        explanation: document.getElementById('questionExplanation').value,
        is_published: true
    };
    
    try {
        const method = id ? 'PUT' : 'POST';
        const url = id ? `${API_BASE}/questions/${id}` : `${API_BASE}/questions`;
        
        await fetch(url, {
            method: method,
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`
            },
            body: JSON.stringify(data)
        });
        
        closeModal();
        loadQuestions();
    } catch (error) {
        alert('保存题目失败: ' + error.message);
    }
}

// ==================== 分类管理 ====================

async function loadCategories() {
    try {
        const response = await fetch(`${API_BASE}/categories`);
        const categories = await response.json();
        
        const list = document.getElementById('categoriesList');
        if (categories.length === 0) {
            list.innerHTML = '<p class="text-center">暂无分类</p>';
            return;
        }
        
        list.innerHTML = categories.map(cat => `
            <div class="category-card">
                <div class="category-info">
                    <h4>${cat.name}</h4>
                    <p>${cat.description || '暂无描述'}</p>
                </div>
                <div class="category-actions">
                    <button class="btn btn-sm" onclick="editCategory(${cat.id})">编辑</button>
                    <button class="btn btn-sm btn-danger" onclick="deleteCategory(${cat.id})">删除</button>
                </div>
            </div>
        `).join('');
    } catch (error) {
        console.error('加载分类失败:', error);
    }
}

function showAddCategoryForm() {
    // 简化处理
    const name = prompt('请输入分类名称:');
    if (!name) return;
    
    handleSaveCategory(null, name);
}

async function handleSaveCategory(id, name) {
    try {
        await fetch(`${API_BASE}/categories`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`
            },
            body: JSON.stringify({ name, description: '' })
        });
        
        loadCategories();
    } catch (error) {
        alert('保存分类失败: ' + error.message);
    }
}

async function deleteCategory(id) {
    if (!confirm('确定要删除这个分类吗？')) return;
    
    try {
        await fetch(`${API_BASE}/categories/${id}`, {
            method: 'DELETE',
            headers: { 'Authorization': `Bearer ${authToken}` }
        });
        loadCategories();
    } catch (error) {
        console.error('删除分类失败:', error);
    }
}

// ==================== 用户统计 ====================

async function loadUsers(page = 1) {
    try {
        const response = await fetch(`${API_BASE}/statistics/users?page=${page}&per_page=20`, {
            headers: { 'Authorization': `Bearer ${authToken}` }
        });
        
        if (response.ok) {
            const data = await response.json();
            renderUsersTable(data.data);
        }
    } catch (error) {
        console.error('加载用户统计失败:', error);
    }
}

function renderUsersTable(users) {
    const tbody = document.getElementById('usersTableBody');
    
    if (users.length === 0) {
        tbody.innerHTML = '<tr><td colspan="5" class="text-center">暂无数据</td></tr>';
        return;
    }
    
    tbody.innerHTML = users.map(user => `
        <tr>
            <td>${user.userId}</td>
            <td>${user.total}</td>
            <td>${user.correct}</td>
            <td>${user.incorrect}</td>
            <td>${user.accuracy}%</td>
        </tr>
    `).join('');
}

// ==================== 账户设置 ====================

async function loadProfile() {
    try {
        const response = await fetch(`${API_BASE}/admin/profile`, {
            headers: { 'Authorization': `Bearer ${authToken}` }
        });
        
        if (response.ok) {
            const admin = await response.json();
            document.getElementById('profileUsername').value = admin.username;
            document.getElementById('profileEmail').value = admin.email || '';
        }
    } catch (error) {
        console.error('加载账户信息失败:', error);
    }
}

async function handleChangePassword() {
    const old = document.getElementById('oldPassword').value;
    const newPass = document.getElementById('newPassword').value;
    const confirm = document.getElementById('confirmPassword').value;
    
    if (!old || !newPass || !confirm) {
        alert('请填写所有字段');
        return;
    }
    
    if (newPass !== confirm) {
        alert('两次输入的密码不一致');
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE}/admin/password`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`
            },
            body: JSON.stringify({
                old_password: old,
                new_password: newPass
            })
        });
        
        if (response.ok) {
            alert('密码已修改');
            document.getElementById('oldPassword').value = '';
            document.getElementById('newPassword').value = '';
            document.getElementById('confirmPassword').value = '';
        } else {
            alert('修改失败: ' + (await response.json()).error);
        }
    } catch (error) {
        alert('修改密码失败: ' + error.message);
    }
}

// ==================== 模态框 ====================

function closeModal() {
    document.getElementById('modal').classList.remove('show');
}

document.querySelector('.modal-close')?.addEventListener('click', closeModal);
