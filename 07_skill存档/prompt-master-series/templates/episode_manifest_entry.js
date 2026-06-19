// 新增一期 = 在 index.html 脚本顶部的 EPISODES 数组里加这样一条对象(放数组末尾即可,首页封面墙自动「最新在前」)。
// 不用再复制 HTML / 改 id / 改 data-target——封面墙、详情页、筛选、点赞计数全部由这条数据驱动。
//
// 占位说明:
//   id        必须唯一,形如 "ep03";同时用作 Abacus 点赞计数 key(命名空间 becoming-a-prompt-master)
//   no        "第 3 期"
//   title     "《主题》"(带书名号)
//   cat       分类 key,须在数组上方的 CATS 里有定义;新分类先在 CATS 加一行 key:{name,color}(颜色复用四色之一)
//   sub       一句话副标题(封面墙不显示,详情页标题下显示)
//   folder    资产文件夹名,如 "03_主题"
//   cover/breakdown/original  三张图文件名(放在 folder 下)
//   note      小白笔记 md 文件名;noteTitle 弹窗标题
//   xhs       小红书帖子链接;留空字符串 "" 则详情页「小红书原帖」按钮自动隐藏
//   prompt    完整 prompt(供「一键复制」)
{
  id:"ep03", no:"第 3 期", title:"《主题》", cat:"object",
  sub:"一句话副标题。",
  folder:"03_主题",
  cover:"主题_封面卡.png", breakdown:"主题_prompt拆解卡.png", original:"主题_原图.png",
  note:"主题_笔记.md", noteTitle:"第 3 期《主题》· 小白笔记",
  xhs:"",
  prompt:"完整 prompt 原文 ..."
}
