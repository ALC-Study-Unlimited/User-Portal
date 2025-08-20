// Article Manager - 記事データの管理を行うモジュール

const ArticleManager = (() => {
  const STORAGE_KEY = 'alcStudyArticles';
  
  // デフォルトの記事データ（最新1記事 + 過去3記事 = 合計4記事）
  const defaultArticles = [
    {
      id: 1,
      url: 'https://ej.alc.co.jp/tag/konare_eigo/sns-insta-droptheball',
      title: '「やらかす」って英語でどう言う？5シーン別に使い分けよう！',
      description: '「やってしまった…！」――そんな失敗やミスをしてしまったとき、英語ではどう表現する？仕事でも日常でも、「やらかした！」という瞬間にぴったりなフレーズがあります。',
      imageUrl: 'https://image-ej.alc.co.jp/images/GKEPd2WZF7WhBSPb1QSCw2.webp',
      date: '最新',
      isFeatured: true
    },
    {
      id: 2,
      url: 'https://ej.alc.co.jp/tag/STUDY/20170517-keinan-10',
      title: 'not much of（あまり～ではない、大した～ではない）を使った表現15',
      description: '「英語5分間トレーニング」などNHKラジオの英語番組を10年担当した英語トレーナー・岩村圭南先生が、英会話が楽しくなる「知って得する」英語表現を紹介！',
      imageUrl: 'https://image-ej.alc.co.jp/images/WSuPNP4Ajgwl6IpxjlAl8K7v.jpeg',
      date: '2017年5月17日',
      isFeatured: false
    },
    {
      id: 3,
      url: 'https://ej.alc.co.jp/tag/konare_eigo/sns-insta-peachy',
      title: '「絶好調」って英語でどう言う？5シーン別に使い分けよう！',
      description: '「今日はツイてる！」そんな日や、何もかも順調に進んでいるとき、英語ではどう表現する？',
      imageUrl: 'https://image-ej.alc.co.jp/images/Qo28XeeteSjU4bEgf.webp',
      date: '学習ヒント',
      isFeatured: false
    },
    {
      id: 4,
      url: 'https://ej.alc.co.jp/tag/STUDY/20190206-shoene-endakazuko-3',
      title: '「以前と比べて2倍に増えた」って英語2語でどう言う？【省エネ英単語】',
      description: '言いたいことを日本語から英語にすると、冗長な英文になってしまう――そんな悩みはありませんか？',
      imageUrl: 'https://image-ej.alc.co.jp/images/xOYdNoRhM1bD52co6kvP4nQD.jpeg',
      date: '2019年2月6日',
      isFeatured: false
    }
  ];

  // LocalStorageから記事データを取得
  const getArticles = () => {
    try {
      const stored = localStorage.getItem(STORAGE_KEY);
      if (stored) {
        return JSON.parse(stored);
      }
    } catch (e) {
      console.error('Failed to load articles from localStorage:', e);
    }
    // デフォルトデータを返す
    return defaultArticles;
  };

  // LocalStorageに記事データを保存
  const saveArticles = (articles) => {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(articles));
      return true;
    } catch (e) {
      console.error('Failed to save articles to localStorage:', e);
      return false;
    }
  };

  // 記事URLから情報を取得（実際のサイトから取得する代わりにモックデータを返す）
  const fetchArticleInfo = async (url) => {
    // 実際の実装では、サーバーサイドのAPIを通じて記事情報を取得する
    // ここではデモのため、URLに基づいてダミーデータを返す
    
    return new Promise((resolve) => {
      setTimeout(() => {
        // URLからタイトルを推測（デモ用）
        const mockData = {
          title: '新しい記事タイトル',
          description: '新しい記事の説明文です。実際の内容はURLから取得されます。',
          imageUrl: 'https://via.placeholder.com/400x250',
          date: new Date().toLocaleDateString('ja-JP')
        };
        
        // 既知のURLパターンをチェック
        if (url.includes('konare_eigo')) {
          mockData.title = '【こなれ英語】シリーズの新記事';
          mockData.description = '日常会話で使える実践的な英語表現を紹介します。';
        } else if (url.includes('STUDY')) {
          mockData.title = '【学習法】効果的な英語学習のヒント';
          mockData.description = '英語学習を効率的に進めるための実践的なアドバイス。';
        }
        
        resolve(mockData);
      }, 500);
    });
  };

  // 記事を更新
  const updateArticle = async (index, url) => {
    const articles = getArticles();
    
    if (index < 0 || index >= articles.length) {
      throw new Error('Invalid article index');
    }
    
    // URLから記事情報を取得
    const articleInfo = await fetchArticleInfo(url);
    
    // 記事データを更新
    articles[index] = {
      ...articles[index],
      url: url,
      title: articleInfo.title,
      description: articleInfo.description,
      imageUrl: articleInfo.imageUrl,
      date: articleInfo.date,
      lastUpdated: new Date().toISOString()
    };
    
    // 保存
    if (saveArticles(articles)) {
      // カスタムイベントを発火して、他のページに更新を通知
      window.dispatchEvent(new CustomEvent('articlesUpdated', { detail: articles }));
      return articles[index];
    }
    
    throw new Error('Failed to save article');
  };

  // 複数の記事を一括更新
  const updateMultipleArticles = async (updates) => {
    const articles = getArticles();
    const updatedArticles = [];
    
    for (const update of updates) {
      if (update.index >= 0 && update.index < articles.length && update.url) {
        const articleInfo = await fetchArticleInfo(update.url);
        
        articles[update.index] = {
          ...articles[update.index],
          url: update.url,
          title: articleInfo.title || update.title || articles[update.index].title,
          description: articleInfo.description || update.description || articles[update.index].description,
          imageUrl: articleInfo.imageUrl || update.imageUrl || articles[update.index].imageUrl,
          date: articleInfo.date || update.date || articles[update.index].date,
          lastUpdated: new Date().toISOString()
        };
        
        updatedArticles.push(articles[update.index]);
      }
    }
    
    if (saveArticles(articles)) {
      window.dispatchEvent(new CustomEvent('articlesUpdated', { detail: articles }));
      return updatedArticles;
    }
    
    throw new Error('Failed to save articles');
  };

  // デフォルトにリセット
  const resetToDefault = () => {
    if (saveArticles(defaultArticles)) {
      window.dispatchEvent(new CustomEvent('articlesUpdated', { detail: defaultArticles }));
      return true;
    }
    return false;
  };

  // 公開API
  return {
    getArticles,
    saveArticles,
    fetchArticleInfo,
    updateArticle,
    updateMultipleArticles,
    resetToDefault
  };
})();

// グローバルに公開
window.ArticleManager = ArticleManager;