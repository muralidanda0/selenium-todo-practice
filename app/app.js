// ============================================================
//  app.js  –  Todo List Application Logic
// ============================================================

const todoInput         = document.getElementById('todo-input');
const addBtn            = document.getElementById('add-btn');
const todoList          = document.getElementById('todo-list');
const itemCount         = document.getElementById('item-count');
const clearCompletedBtn = document.getElementById('clear-completed-btn');
const emptyMsg          = document.getElementById('empty-msg');
const errorMsg          = document.getElementById('error-msg');
const filterBtns        = document.querySelectorAll('.filter-btn');

let todos        = [];
let currentFilter = 'all';

// ---- Helpers ------------------------------------------------

function showError(msg) {
  errorMsg.textContent = msg;
  errorMsg.style.display = 'block';
  setTimeout(() => { errorMsg.style.display = 'none'; }, 3000);
}

function getRandomPriority() {
  const priorities = ['high', 'medium', 'low'];
  return priorities[Math.floor(Math.random() * priorities.length)];
}

// ---- Render -------------------------------------------------

function render() {
  const filtered = todos.filter(t => {
    if (currentFilter === 'active') return !t.done;
    if (currentFilter === 'done')   return  t.done;
    return true;
  });

  todoList.innerHTML = '';

  filtered.forEach(todo => {
    const li = document.createElement('li');
    li.className  = `todo-item${todo.done ? ' completed' : ''}`;
    li.dataset.id = todo.id;

    li.innerHTML = `
      <input type="checkbox" class="todo-checkbox" id="cb-${todo.id}" ${todo.done ? 'checked' : ''} aria-label="Mark done" />
      <label class="todo-text" for="cb-${todo.id}">${escapeHtml(todo.text)}</label>
      <span class="priority-badge priority-${todo.priority}">${todo.priority}</span>
      <button class="delete-btn" data-id="${todo.id}" aria-label="Delete task">✕</button>
    `;

    todoList.appendChild(li);
  });

  // empty message
  const remaining = todos.filter(t => !t.done).length;
  emptyMsg.classList.toggle('visible', filtered.length === 0);
  itemCount.textContent = `${remaining} task${remaining !== 1 ? 's' : ''} remaining`;
}

function escapeHtml(str) {
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

// ---- Add Todo -----------------------------------------------

function addTodo() {
  const text = todoInput.value.trim();

  if (!text) {
    showError('Task cannot be empty!');
    return;
  }
  if (text.length > 100) {
    showError('Task must be 100 characters or fewer.');
    return;
  }
  if (todos.some(t => t.text.toLowerCase() === text.toLowerCase())) {
    showError('This task already exists!');
    return;
  }

  todos.push({
    id:       Date.now(),
    text:     text,
    done:     false,
    priority: getRandomPriority(),
  });

  todoInput.value = '';
  errorMsg.style.display = 'none';
  render();
}

// ---- Toggle / Delete ----------------------------------------

todoList.addEventListener('click', e => {
  const id = Number(e.target.dataset.id || e.target.closest('[data-id]')?.dataset.id);

  if (e.target.classList.contains('todo-checkbox')) {
    const todo = todos.find(t => t.id === id);
    if (todo) { todo.done = !todo.done; render(); }
  }

  if (e.target.classList.contains('delete-btn')) {
    todos = todos.filter(t => t.id !== id);
    render();
  }
});

// ---- Clear Completed ----------------------------------------

clearCompletedBtn.addEventListener('click', () => {
  todos = todos.filter(t => !t.done);
  render();
});

// ---- Filters ------------------------------------------------

filterBtns.forEach(btn => {
  btn.addEventListener('click', () => {
    filterBtns.forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    currentFilter = btn.id.replace('filter-', '');
    render();
  });
});

// ---- Events -------------------------------------------------

addBtn.addEventListener('click', addTodo);
todoInput.addEventListener('keydown', e => {
  if (e.key === 'Enter') addTodo();
});

// ---- Init ---------------------------------------------------

render();
