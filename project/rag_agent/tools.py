from langchain_core.tools import tool
import config
from db.parent_store_manager import ParentStoreManager
from core.execution_logger import log_error, log_tool_end, log_tool_start

class ToolFactory:
    
    def __init__(self, collection):
        self.collection = collection
        self.parent_store_manager = ParentStoreManager()
    
    def _search_child_chunks(self, query: str, limit: int = config.DEFAULT_RETRIEVAL_K) -> str:
        """Search document excerpts for evidence related to the user question.

        Use this as the first retrieval step. Results include parent IDs, file
        names, and short child-chunk excerpts. If excerpts are relevant but too
        fragmented to answer confidently, call retrieve_parent_chunks with the
        returned parent_id.
        
        Args:
            query: Focused search query with concrete keywords from the question.
            limit: Maximum number of child chunks to return.
        """
        log_tool_start("search_child_chunks", {"query": query, "limit": limit})
        try:
            results = self.collection.similarity_search(
                query,
                k=limit,
                score_threshold=config.RETRIEVAL_SCORE_THRESHOLD,
            )
            if not results:
                output = "NO_RELEVANT_CHUNKS"
                log_tool_end("search_child_chunks", output)
                return output

            output = config.CHILD_CHUNK_SEPARATOR.join([
                f"Parent ID: {doc.metadata.get('parent_id', '')}\n"
                f"File Name: {doc.metadata.get('source', '')}\n"
                f"Content: {doc.page_content.strip()}"
                for doc in results
            ])
            log_tool_end("search_child_chunks", output)
            return output

        except Exception as e:
            log_error("search_child_chunks", e)
            output = f"RETRIEVAL_ERROR: {str(e)}"
            log_tool_end("search_child_chunks", output)
            return output
    
    def _retrieve_parent_chunks(self, parent_id: str) -> str:
        """Retrieve the full parent chunk for a relevant child search result.

        Use this only after search_child_chunks returns a relevant parent_id and
        the child excerpt needs more surrounding context. Do not call this for
        parent IDs already available in compressed context.
    
        Args:
            parent_id: Parent chunk ID returned by search_child_chunks.
        """
        log_tool_start("retrieve_parent_chunks", {"parent_id": parent_id})
        try:
            parent = self.parent_store_manager.load_content(parent_id)
            if not parent:
                output = "NO_PARENT_DOCUMENT"
                log_tool_end("retrieve_parent_chunks", output)
                return output

            output = (
                f"Parent ID: {parent.get('parent_id', 'n/a')}\n"
                f"File Name: {parent.get('metadata', {}).get('source', 'unknown')}\n"
                f"Content: {parent.get('content', '').strip()}"
            )
            log_tool_end("retrieve_parent_chunks", output)
            return output

        except Exception as e:
            log_error("retrieve_parent_chunks", e)
            output = f"PARENT_RETRIEVAL_ERROR: {str(e)}"
            log_tool_end("retrieve_parent_chunks", output)
            return output
    
    def _web_search(self, query: str) -> str:
        """Search the public web for general or market context the documents do not cover
        (for example salary benchmarks, standards, current events).

        Use this ONLY after the document tools have returned nothing relevant. Anything
        drawn from this tool is outside evidence: in the final answer, put it under a
        heading "Estimate (not from your documents)" and name it as an estimate.

        Args:
            query: A focused web query.
        """
        log_tool_start("web_search", {"query": query})
        try:
            from ddgs import DDGS
            n = getattr(config, "WEB_SEARCH_MAX_RESULTS", 5)
            with DDGS() as ddgs:
                hits = list(ddgs.text(query, max_results=n))
            if not hits:
                out = "NO_WEB_RESULTS"
            else:
                out = "\n\n".join(
                    f"{h.get('title', '')}\n{h.get('href', '')}\n{h.get('body', '')}" for h in hits
                )
            log_tool_end("web_search", out)
            return out
        except Exception as e:
            log_error("web_search", e)
            out = f"WEB_SEARCH_ERROR: {str(e)}"
            log_tool_end("web_search", out)
            return out

    def create_tools(self) -> list:
        """Create and return the list of tools."""
        tools = [
            tool("search_child_chunks")(self._search_child_chunks),
            tool("retrieve_parent_chunks")(self._retrieve_parent_chunks),
        ]
        if getattr(config, "WEB_SEARCH_ENABLED", False):
            tools.append(tool("web_search")(self._web_search))
        return tools
