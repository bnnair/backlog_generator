# database.py
import sqlite3
import os
from pathlib import Path
from datetime import datetime
from contextlib import contextmanager
from typing import List, Dict, Any, Optional
from utils.logger import get_logger

logger = get_logger(__name__)   

class RequirementsDatabase:
    def __init__(self):
        parent_dir = Path(__file__).parent.parent
        db_path = os.path.join(parent_dir,"database","requirements.db")
        logger.info(f"db_path : {db_path}")
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        """Initialize the database with required tables"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Projects table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS projects (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    description TEXT,
                    user_requirements TEXT,
                    tech_stack TEXT,
                    status TEXT DEFAULT 'draft',
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Requirements documents table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS requirement_documents (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    project_id INTEGER,
                    content TEXT,
                    version INTEGER DEFAULT 1,
                    created_by TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (project_id) REFERENCES projects (id)
                )
            ''')
            
            # Product backlog items table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS backlog_items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    project_id INTEGER,
                    requirement_doc_id INTEGER,
                    backlog_content TEXT NOT NULL,
                    status TEXT DEFAULT 'draft',
                    created_by TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (project_id) REFERENCES projects (id),
                    FOREIGN KEY (requirement_doc_id) REFERENCES requirement_documents (id)
                )
            ''')
            
            # Review feedback table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS review_feedback (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    project_id INTEGER,
                    backlog_item_id INTEGER,
                    iteration_id INTEGER,
                    feedback TEXT,
                    action_required TEXT,
                    status TEXT DEFAULT 'open',
                    created_by TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    resolved_at DATETIME,
                    FOREIGN KEY (project_id) REFERENCES projects (id),
                    FOREIGN KEY (backlog_item_id) REFERENCES backlog_items (id)
                )
            ''')
            
            # # Agent conversations table
            # cursor.execute('''
            #     CREATE TABLE IF NOT EXISTS agent_conversations (
            #         id INTEGER PRIMARY KEY AUTOINCREMENT,
            #         project_id INTEGER,
            #         from_agent TEXT,
            #         to_agent TEXT,
            #         message TEXT,
            #         message_type TEXT,
            #         created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            #         FOREIGN KEY (project_id) REFERENCES projects (id)
            #     )
            # ''')
            
            conn.commit()
    
    
    @contextmanager
    def transaction(self):
        """Context manager for transaction handling"""
        conn = sqlite3.connect(self.db_path)
        conn.execute("BEGIN TRANSACTION")
        try:
            yield conn
            conn.commit()
            logger.info("Transaction committed successfully")
        except Exception as e:
            conn.rollback()
            logger.error(f"Transaction rolled back due to error: {e}")
            raise
        finally:
            conn.close()
    
    
    def create_project(self, name: str, description: str, user_requirements: str, tech_stack: str) -> int:
        """Create a new project"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO projects (name, description, user_requirements, tech_stack) VALUES (?, ?, ?, ?)",
                    (name, description, user_requirements, tech_stack)
                )
                conn.commit()
                
        except sqlite3.Error as e:
            logger.error(f"Database connection error: {str(e)}")
            raise

        except Exception as e:
            logger.error(
                f"Unexpected error when creating project : {str(e)}", 
                exc_info=True,  # This will include stack trace
            )
        finally:
            if conn:
                conn.close()

        return cursor.lastrowid
    
    def save_requirement_document(self, project_id: int, content: str, created_by: str) -> int:
        """Save a requirement document"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO requirement_documents (project_id, content, created_by) VALUES (?, ?, ?)",
                    (project_id, content, created_by)
                )
                conn.commit()

        except sqlite3.Error as e:
            logger.error(f"Database connection error: {str(e)}")
            raise
        
        except Exception as e:
            logger.error(
                f"Unexpected error when saving requirement document : {str(e)}", 
                exc_info=True,  # This will include stack trace
            )

        finally:
            if conn:
                conn.close()

        return cursor.lastrowid
    
    def add_backlog_item(self, project_id: int, requirement_doc_id: int, backlog: str,  created_by: str) -> int:
        """Add a backlog item"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """INSERT INTO backlog_items 
                    (project_id, requirement_doc_id, backlog_content, created_by) 
                    VALUES (?, ?, ?, ?)""",
                    (project_id, requirement_doc_id, backlog, created_by)
                )
                conn.commit()
            
        except sqlite3.Error as e:
            logger.error(f"Database connection error: {str(e)}")
            raise
        
        except Exception as e:
            logger.error(
                f"Unexpected error when adding backlog document : {str(e)}", 
                exc_info=True,  # This will include stack trace
            )

        finally:
            if conn:
                conn.close()            
        return cursor.lastrowid
    
    def add_review_feedback(self, iteration_id: int, project_id: int, backlog_item_id: int, 
                           feedback: str, action_required: str, created_by: str) -> int:
        """Add review feedback for a backlog item"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """INSERT INTO review_feedback 
                    (project_id, backlog_item_id, iteration_id, feedback, action_required, created_by) 
                    VALUES (?, ?, ?, ?, ?, ?)""",
                    (project_id, backlog_item_id, iteration_id, feedback, action_required, created_by)
                )
                conn.commit()
            
        except sqlite3.Error as e:
            logger.error(f"Database connection error: {str(e)}")
            raise
        except Exception as e:
            logger.error(
                f"Unexpected error when adding review feedback : {str(e)}", 
                exc_info=True,  # This will include stack trace
            )
        finally:
            if conn:
                conn.close()
                            
        return cursor.lastrowid
    
    def get_backlog_id(self):
        ## get the latest backlog id from the database
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute("SELECT id FROM backlog_items ORDER BY id DESC LIMIT 1")
                row = cursor.fetchone()
                return row["id"] if row else None
        except sqlite3.Error as e:
            logger.error(f"Database connection error: {str(e)}")
            raise
        except Exception as e:
            logger.error(
                f"Unexpected error when getting latest backlog id : {str(e)}", 
                exc_info=True,  # This will include stack trace
            )
    
    
    def get_backlog_item(self, backlog_id) -> Optional[Dict[str, Any]]:
        """Get a backlog item by ID"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM backlog_items WHERE id = ?", (backlog_id,))
                row = cursor.fetchone()
        
        except sqlite3.Error as e:
            logger.error(f"Database connection error: {str(e)}")
            raise
        except Exception as e:
            logger.error(
                f"Unexpected error when getting backlog item : {str(e)}", 
                exc_info=True,  # This will include stack trace
            )
        finally:
            if conn:
                conn.close()
        
        return dict(row) if row else None


    def get_latest_feedback_iteration(self, backlog_id: int) -> int:
        """Get the latest iteration ID for feedback on a backlog item"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT MAX(iteration_id) as max_iteration FROM review_feedback WHERE backlog_item_id = ?",
                    (backlog_id,)
                )
                row = cursor.fetchone()
                return row["max_iteration"] if row and row["max_iteration"] is not None else 0
        
        except sqlite3.Error as e:
            logger.error(f"Database connection error: {str(e)}")
            raise
        except Exception as e:
            logger.error(
                f"Unexpected error when getting latest feedback iteration : {str(e)}", 
                exc_info=True,  # This will include stack trace
            )
        finally:
            if conn:
                conn.close()
        
        return 0

    
    def get_project(self, project_id: int) -> Optional[Dict[str, Any]]:
        """Get project details"""
        try:

            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM projects WHERE id = ?", (project_id,))
                row = cursor.fetchone()
            
        except sqlite3.Error as e:
            logger.error(f"Database connection error: {str(e)}")
            raise
        
        except Exception as e:
            logger.error(
                f"Unexpected error when getting project : {str(e)}", 
                exc_info=True,  # This will include stack trace
            )

        finally:
            if conn:
                conn.close()
        
        return dict(row) if row else None
    
    def get_requirement_document(self, project_id: int) -> Optional[Dict[str, Any]]:
        """Get the latest requirement document for a project"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute(
                    """SELECT * FROM requirement_documents 
                    WHERE project_id = ? ORDER BY version DESC LIMIT 1""",
                    (project_id,)
                )
                row = cursor.fetchone()
        
        except sqlite3.Error as e:
            logger.error(f"Database connection error: {str(e)}")
            raise
        
        except Exception as e:
            logger.error(
                f"Unexpected error when retrieving requirement document : {str(e)}", 
                exc_info=True,  # This will include stack trace
            )

        finally:
            if conn:
                conn.close()
        
        return dict(row) if row else None
    
    def get_backlog_items(self, project_id: int) -> List[Dict[str, Any]]:
        """Get all backlog items for a project"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT * FROM backlog_items WHERE project_id = ? ORDER BY priority, id",
                    (project_id,)
                )
        
        except sqlite3.Error as e:
            logger.error(f"Database connection error: {str(e)}")
            raise
        
        except Exception as e:
            logger.error(
                f"Unexpected error when retrieving backlog items : {str(e)}", 
                exc_info=True,  # This will include stack trace
            )

        finally:
            if conn:
                conn.close()
        
        return [dict(row) for row in cursor.fetchall()]
    
    def get_review_feedback(self, project_id: int, status: str = "open") -> List[Dict[str, Any]]:
        """Get review feedback for a project"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute(
                    """SELECT * FROM review_feedback 
                    WHERE project_id = ? AND status = ? ORDER BY created_at""",
                    (project_id, status)
                )
        
        except sqlite3.Error as e:
            logger.error(f"Database connection error: {str(e)}")
            raise
        
        except Exception as e:
            logger.error(
                f"Unexpected error when retrieving review feedback : {str(e)}", 
                exc_info=True,  # This will include stack trace
            )

        finally:
            if conn:
                conn.close()
        
        return [dict(row) for row in cursor.fetchall()]
    
    def update_backlog_item(self, item_id: int, backlog_items: str):
        """Update a backlog item"""

        if not backlog_items:
            return
        
        values = item_id
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE backlog_items SET backlog_content = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                            (backlog_items, values))
                conn.commit()

        except sqlite3.Error as e:
            logger.error(f"Database connection error: {str(e)}")
            raise
        
        except Exception as e:
            logger.error(
                f"Unexpected error when updating backlog document : {str(e)}", 
                exc_info=True,  # This will include stack trace
            )

        finally:
            if conn:
                conn.close()

    
    def resolve_feedback(self, feedback_id: int):
        """Mark feedback as resolved"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE review_feedback SET status = 'resolved', resolved_at = CURRENT_TIMESTAMP WHERE id = ?",
                    (feedback_id,)
                )
                conn.commit()
                
        except sqlite3.Error as e:
            logger.error(f"Database connection error: {str(e)}")
            raise
        
        except Exception as e:
            logger.error(
                f"Unexpected error when updating the review feedback: {str(e)}", 
                exc_info=True,  # This will include stack trace
            )

        finally:
            if conn:
                conn.close()