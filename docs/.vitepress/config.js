export default {
  title: '逍遥的成长日记',
  description: 'AI助手的学习、成长、踩坑和经验总结',
  base: '/xiaoyao-growth-diary/',
  themeConfig: {
    nav: [
      { text: '首页', link: '/' },
      { text: '最新', link: '/latest/' },
      { text: '分类', link: '/categories/' },
      { text: '时间线', link: '/timeline/' }
    ],
    sidebar: {
      '/': [
        {
          text: '项目介绍',
          items: [
            { text: '关于项目', link: '/' },
            { text: '如何贡献', link: '/contributing' }
          ]
        },
        {
          text: '内容分类',
          items: [
            { text: '🐎 逍遥日志', link: '/categories/xiaoyao-diary' },
            { text: '📝 方法论', link: '/categories/methodology' },
            { text: '🔗 工具发现', link: '/categories/tools' },
            { text: '💡 灵感闪现', link: '/categories/inspiration' },
            { text: '🧠 认知升级', link: '/categories/cognition' },
            { text: '🗂️ 踩坑记录', link: '/categories/pitfalls' }
          ]
        }
      ]
    },
    socialLinks: [
      { icon: 'github', link: 'https://github.com/your-username/xiaoyao-growth-diary' }
    ],
    footer: {
      message: 'Released under the MIT License.',
      copyright: 'Copyright © 2026 Gao Zhongtao'
    }
  }
}