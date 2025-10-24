"""
Flask Backend API for React Calculator
======================================

REST API to connect React calculator with PostgreSQL database.
Provides endpoints for saving calculations, retrieving history, and managing sessions.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import uuid
from datetime import datetime
from database_helper import CalculatorDB, save_calculation, get_history, clear_history
import json

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Global database instance
db = CalculatorDB()

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'Calculator API is running',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/calculate', methods=['POST'])
def save_calculation_endpoint():
    """Save a calculation to the database"""
    try:
        data = request.get_json()
        
        if not data or 'expression' not in data or 'result' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing expression or result'
            }), 400
        
        expression = data['expression']
        result = data['result']
        session_id = data.get('session_id', str(uuid.uuid4()))
        
        # Save to database
        success = save_calculation(expression, result, session_id)
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Calculation saved successfully',
                'session_id': session_id
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to save calculation'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/history', methods=['GET'])
def get_calculation_history():
    """Get calculation history"""
    try:
        limit = request.args.get('limit', 50, type=int)
        history = get_history(limit)
        
        # Format history for frontend
        formatted_history = []
        for record in history:
            formatted_history.append({
                'id': record[0],
                'expression': record[1],
                'result': record[2],
                'timestamp': record[3].isoformat()
            })
        
        return jsonify({
            'success': True,
            'history': formatted_history,
            'count': len(formatted_history)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/history/clear', methods=['POST'])
def clear_calculation_history():
    """Clear all calculation history"""
    try:
        success = clear_history()
        
        if success:
            return jsonify({
                'success': True,
                'message': 'History cleared successfully'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to clear history'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/session', methods=['POST'])
def create_session():
    """Create a new calculator session"""
    try:
        session_id = str(uuid.uuid4())
        success = db.create_session(session_id)
        
        if success:
            return jsonify({
                'success': True,
                'session_id': session_id,
                'message': 'Session created successfully'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to create session'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/session/<session_id>/stats', methods=['GET'])
def get_session_stats(session_id):
    """Get statistics for a session"""
    try:
        stats = db.get_session_stats(session_id)
        
        if stats:
            return jsonify({
                'success': True,
                'stats': {
                    'total_calculations': stats['total_calculations'],
                    'created_at': stats['created_at'].isoformat(),
                    'last_used': stats['last_used'].isoformat()
                }
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Session not found'
            }), 404
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/stats', methods=['GET'])
def get_overall_stats():
    """Get overall calculation statistics"""
    try:
        history = get_history(limit=1000)
        
        if not history:
            return jsonify({
                'success': True,
                'stats': {
                    'total_calculations': 0,
                    'operations': {'+': 0, '-': 0, '*': 0, '/': 0},
                    'date_range': None
                }
            })
        
        # Count operations
        operations = {'+': 0, '-': 0, '*': 0, '/': 0}
        for record in history:
            expression = record[1]
            for op in operations:
                operations[op] += expression.count(op)
        
        # Get date range
        timestamps = [record[3] for record in history]
        date_range = {
            'oldest': min(timestamps).isoformat(),
            'newest': max(timestamps).isoformat()
        }
        
        return jsonify({
            'success': True,
            'stats': {
                'total_calculations': len(history),
                'operations': operations,
                'date_range': date_range
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500

if __name__ == '__main__':
    print("Starting Calculator API Server...")
    print("API Endpoints:")
    print("  GET  /api/health - Health check")
    print("  POST /api/calculate - Save calculation")
    print("  GET  /api/history - Get calculation history")
    print("  POST /api/history/clear - Clear history")
    print("  POST /api/session - Create session")
    print("  GET  /api/session/<id>/stats - Get session stats")
    print("  GET  /api/stats - Get overall statistics")
    print("\nServer starting on http://localhost:5000")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
