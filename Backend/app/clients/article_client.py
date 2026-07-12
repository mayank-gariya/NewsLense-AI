import trafilatura

from app.utils.logger import logger

class ArticleClient:
    def extract_article(
        self,
        url: str
    ) -> str | None:

        try:
            downloaded = trafilatura.fetch_url(url)

            if downloaded is None:
                logger.warning(
                    f"Unable to download article: {url}"
                )
                return None

            article = trafilatura.extract(
                downloaded,
                include_comments=False,
                include_tables=False
            )

            if not article:
                logger.warning(
                    f"No article extracted: {url}"
                )
                return None

            logger.info(
                f"Article extracted successfully."
            )
            return article.strip()

        except Exception as e:
            logger.exception(
                f"Article extraction failed: {e}"
            )
            return None