# services/realtime_notifications.py - Advanced Real-time Notification System
import asyncio
import json
import websockets
import logging
from typing import Dict, List, Any, Optional, Set
from datetime import datetime, timedelta
import uuid
from collections import defaultdict
import threading
import time
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

logger = logging.getLogger(__name__)

class AdvancedRealtimeNotifications:
    def __init__(self):
        """Initialize the advanced real-time notification system"""
        # WebSocket connections management
        self.active_connections: Dict[int, Set[websockets.WebSocketServerProtocol]] = defaultdict(set)
        self.connection_metadata: Dict[websockets.WebSocketServerProtocol, Dict] = {}

        # Notification queues and history
        self.notification_queues: Dict[int, asyncio.Queue] = defaultdict(asyncio.Queue)
        self.notification_history: Dict[int, List[Dict]] = defaultdict(list)

        # Scheduled notifications
        self.scheduler = AsyncIOScheduler()
        self.scheduled_jobs = {}

        # Notification types and templates
        self.notification_types = {
            'job_match': {
                'priority': 'high',
                'icon': '💼',
                'sound': 'job_match',
                'template': 'New job match: {job_title} at {company}'
            },
            'application_update': {
                'priority': 'high',
                'icon': '📋',
                'sound': 'application_update',
                'template': 'Your application for {job_title} has been {status}'
            },
            'interview_invite': {
                'priority': 'urgent',
                'icon': '📅',
                'sound': 'interview_invite',
                'template': 'Interview scheduled for {job_title} on {date} at {time}'
            },
            'skill_recommendation': {
                'priority': 'medium',
                'icon': '🎯',
                'sound': 'skill_recommendation',
                'template': 'Recommended skill: {skill_name} - {reason}'
            },
            'market_alert': {
                'priority': 'medium',
                'icon': '📈',
                'sound': 'market_alert',
                'template': '{skill} jobs increased by {percentage}% this month'
            },
            'career_insight': {
                'priority': 'low',
                'icon': '💡',
                'sound': 'career_insight',
                'template': 'Career tip: {insight}'
            },
            'system_update': {
                'priority': 'low',
                'icon': '🔄',
                'sound': 'system_update',
                'template': 'System update: {message}'
            }
        }

        # User preferences
        self.user_preferences: Dict[int, Dict[str, Any]] = defaultdict(dict)

        # Start background tasks
        self._start_background_tasks()

        print("✅ Advanced Real-time Notifications initialized!")

    def _start_background_tasks(self):
        """Start background notification processing tasks"""
        # Start scheduler for periodic notifications
        self.scheduler.start()

        # Schedule daily market insights
        self.scheduler.add_job(
            self._send_daily_market_insights,
            trigger=IntervalTrigger(hours=24),
            id='daily_market_insights',
            replace_existing=True
        )

        # Schedule skill recommendations
        self.scheduler.add_job(
            self._send_weekly_skill_recommendations,
            trigger=IntervalTrigger(hours=168),  # Weekly
            id='weekly_skill_recommendations',
            replace_existing=True
        )

    async def connect(self, websocket: websockets.WebSocketServerProtocol, user_id: int):
        """Handle new WebSocket connection"""
        # Add to active connections
        self.active_connections[user_id].add(websocket)
        self.connection_metadata[websocket] = {
            'user_id': user_id,
            'connected_at': datetime.utcnow(),
            'last_activity': datetime.utcnow()
        }

        logger.info(f"🔗 User {user_id} connected. Total connections: {len(self.active_connections[user_id])}")

        # Send welcome message
        await self._send_notification_to_connection(
            websocket,
            'system_update',
            {'message': 'Connected to Green Matchers real-time notifications'}
        )

        # Send any queued notifications
        await self._send_queued_notifications(user_id, websocket)

    async def disconnect(self, websocket: websockets.WebSocketServerProtocol):
        """Handle WebSocket disconnection"""
        if websocket in self.connection_metadata:
            user_id = self.connection_metadata[websocket]['user_id']

            # Remove from active connections
            self.active_connections[user_id].discard(websocket)
            del self.connection_metadata[websocket]

            # Clean up empty connection sets
            if not self.active_connections[user_id]:
                del self.active_connections[user_id]

            logger.info(f"🔌 User {user_id} disconnected. Remaining connections: {len(self.active_connections.get(user_id, set()))}")

    async def send_notification(self, user_id: int, notification_type: str,
                              data: Dict[str, Any], priority: str = None) -> bool:
        """Send notification to user"""
        try:
            # Check user preferences
            if not self._should_send_notification(user_id, notification_type):
                return False

            # Format notification
            notification = self._format_notification(notification_type, data, priority)

            # Add to history
            self.notification_history[user_id].append({
                **notification,
                'timestamp': datetime.utcnow(),
                'read': False
            })

            # Keep only last 100 notifications
            self.notification_history[user_id] = self.notification_history[user_id][-100:]

            # Send to active connections
            success = await self._broadcast_to_user(user_id, notification)

            # Queue if no active connections
            if not success:
                await self.notification_queues[user_id].put(notification)

            # Trigger any follow-up actions
            await self._trigger_notification_actions(user_id, notification_type, data)

            logger.info(f"📤 Sent {notification_type} notification to user {user_id}")
            return True

        except Exception as e:
            logger.error(f"Failed to send notification to user {user_id}: {e}")
            return False

    async def broadcast_to_all(self, notification_type: str, data: Dict[str, Any],
                             user_filter: Optional[Dict] = None):
        """Broadcast notification to multiple users"""
        try:
            notification = self._format_notification(notification_type, data)

            # Apply user filter if provided
            target_users = self._get_filtered_users(user_filter) if user_filter else list(self.active_connections.keys())

            success_count = 0
            for user_id in target_users:
                if await self.send_notification(user_id, notification_type, data):
                    success_count += 1

            logger.info(f"📢 Broadcast {notification_type} to {success_count}/{len(target_users)} users")
            return success_count

        except Exception as e:
            logger.error(f"Broadcast failed: {e}")
            return 0

    async def get_user_notifications(self, user_id: int, limit: int = 50,
                                   unread_only: bool = False) -> List[Dict]:
        """Get user's notification history"""
        notifications = self.notification_history.get(user_id, [])

        if unread_only:
            notifications = [n for n in notifications if not n.get('read', False)]

        # Sort by timestamp (newest first)
        notifications.sort(key=lambda x: x['timestamp'], reverse=True)

        return notifications[:limit]

    async def mark_notifications_read(self, user_id: int, notification_ids: List[str]):
        """Mark specific notifications as read"""
        for notification in self.notification_history.get(user_id, []):
            if notification.get('id') in notification_ids:
                notification['read'] = True

    def update_user_preferences(self, user_id: int, preferences: Dict[str, Any]):
        """Update user's notification preferences"""
        self.user_preferences[user_id].update(preferences)

    def get_user_preferences(self, user_id: int) -> Dict[str, Any]:
        """Get user's notification preferences"""
        return self.user_preferences.get(user_id, {
            'email_notifications': True,
            'push_notifications': True,
            'sms_notifications': False,
            'notification_types': {
                'job_match': True,
                'application_update': True,
                'interview_invite': True,
                'skill_recommendation': True,
                'market_alert': False,
                'career_insight': True,
                'system_update': False
            }
        })

    async def _broadcast_to_user(self, user_id: int, notification: Dict) -> bool:
        """Broadcast notification to all user's active connections"""
        if user_id not in self.active_connections:
            return False

        success = False
        for websocket in self.active_connections[user_id].copy():
            try:
                await self._send_notification_to_connection(websocket, notification)
                success = True
            except Exception as e:
                logger.warning(f"Failed to send to connection: {e}")
                # Remove dead connection
                self.active_connections[user_id].discard(websocket)
                if websocket in self.connection_metadata:
                    del self.connection_metadata[websocket]

        return success

    async def _send_notification_to_connection(self, websocket: websockets.WebSocketServerProtocol,
                                            notification: Dict):
        """Send notification to specific WebSocket connection"""
        try:
            await websocket.send(json.dumps({
                'type': 'notification',
                'data': notification,
                'timestamp': datetime.utcnow().isoformat()
            }))

            # Update last activity
            if websocket in self.connection_metadata:
                self.connection_metadata[websocket]['last_activity'] = datetime.utcnow()

        except Exception as e:
            logger.error(f"WebSocket send failed: {e}")
            raise

    async def _send_queued_notifications(self, user_id: int, websocket: websockets.WebSocketServerProtocol):
        """Send queued notifications to newly connected client"""
        queue = self.notification_queues.get(user_id)
        if not queue:
            return

        sent_count = 0
        try:
            while not queue.empty() and sent_count < 10:  # Limit to prevent spam
                notification = queue.get_nowait()
                await self._send_notification_to_connection(websocket, notification)
                sent_count += 1
        except asyncio.QueueEmpty:
            pass

        if sent_count > 0:
            logger.info(f"📨 Sent {sent_count} queued notifications to user {user_id}")

    def _format_notification(self, notification_type: str, data: Dict[str, Any],
                           priority: str = None) -> Dict[str, Any]:
        """Format notification with metadata"""
        template_config = self.notification_types.get(notification_type, {})

        # Generate notification text
        template = template_config.get('template', '{message}')
        try:
            message = template.format(**data)
        except KeyError:
            message = data.get('message', f'New {notification_type} notification')

        return {
            'id': str(uuid.uuid4()),
            'type': notification_type,
            'message': message,
            'data': data,
            'priority': priority or template_config.get('priority', 'medium'),
            'icon': template_config.get('icon', '📢'),
            'sound': template_config.get('sound', 'default'),
            'timestamp': datetime.utcnow(),
            'read': False,
            'actions': self._get_notification_actions(notification_type, data)
        }

    def _get_notification_actions(self, notification_type: str, data: Dict) -> List[Dict]:
        """Get available actions for notification"""
        actions = []

        if notification_type == 'job_match':
            actions.extend([
                {'label': 'View Job', 'action': 'view_job', 'data': {'job_id': data.get('job_id')}},
                {'label': 'Apply Now', 'action': 'apply_job', 'data': {'job_id': data.get('job_id')}},
                {'label': 'Save for Later', 'action': 'save_job', 'data': {'job_id': data.get('job_id')}}
            ])
        elif notification_type == 'application_update':
            actions.append({
                'label': 'View Application',
                'action': 'view_application',
                'data': {'application_id': data.get('application_id')}
            })
        elif notification_type == 'interview_invite':
            actions.extend([
                {'label': 'Accept Interview', 'action': 'accept_interview', 'data': {'interview_id': data.get('interview_id')}},
                {'label': 'View Details', 'action': 'view_interview', 'data': {'interview_id': data.get('interview_id')}}
            ])

        return actions

    def _should_send_notification(self, user_id: int, notification_type: str) -> bool:
        """Check if notification should be sent based on user preferences"""
        preferences = self.get_user_preferences(user_id)
        return preferences.get('notification_types', {}).get(notification_type, True)

    async def _trigger_notification_actions(self, user_id: int, notification_type: str, data: Dict):
        """Trigger follow-up actions based on notification type"""
        if notification_type == 'job_match':
            # Trigger similar job recommendations
            await self._schedule_similar_jobs_notification(user_id, data)

        elif notification_type == 'application_update':
            # Trigger next steps guidance
            await self._schedule_application_followup(user_id, data)

        elif notification_type == 'interview_invite':
            # Trigger interview preparation tips
            await self._schedule_interview_prep_notification(user_id, data)

    async def _schedule_similar_jobs_notification(self, user_id: int, job_data: Dict):
        """Schedule notification about similar jobs"""
        await asyncio.sleep(300)  # 5 minutes later

        similar_jobs = await self._find_similar_jobs(job_data)
        if similar_jobs:
            await self.send_notification(
                user_id,
                'job_match',
                {
                    'message': f"Found {len(similar_jobs)} similar jobs to the one you viewed",
                    'similar_jobs': similar_jobs
                },
                'medium'
            )

    async def _schedule_application_followup(self, user_id: int, application_data: Dict):
        """Schedule follow-up after application"""
        await asyncio.sleep(86400)  # 24 hours later

        await self.send_notification(
            user_id,
            'career_insight',
            {
                'insight': 'Follow up on your job application in 3-5 business days if you haven\'t heard back.',
                'tip_type': 'application_followup'
            },
            'low'
        )

    async def _schedule_interview_prep_notification(self, user_id: int, interview_data: Dict):
        """Schedule interview preparation tips"""
        await asyncio.sleep(3600)  # 1 hour later

        await self.send_notification(
            user_id,
            'career_insight',
            {
                'insight': 'Practice common interview questions and prepare your success stories. Good luck!',
                'tip_type': 'interview_preparation'
            },
            'medium'
        )

    async def _find_similar_jobs(self, job_data: Dict) -> List[Dict]:
        """Find similar jobs for recommendations"""
        try:
            from ..vector_services import vector_service
            similar_jobs = vector_service.semantic_search_jobs(
                job_data.get('skills', ''),
                top_k=3
            )
            return similar_jobs
        except Exception as e:
            logger.error(f"Similar jobs search failed: {e}")
            return []

    def _get_filtered_users(self, user_filter: Dict) -> List[int]:
        """Get users matching filter criteria"""
        # This would integrate with user database
        # For now, return all connected users
        return list(self.active_connections.keys())

    async def _send_daily_market_insights(self):
        """Send daily market insights to all users"""
        try:
            # Get market data
            market_data = await self._get_market_insights()

            # Send to users who have market alerts enabled
            sent_count = 0
            for user_id in list(self.active_connections.keys()):
                preferences = self.get_user_preferences(user_id)
                if preferences.get('notification_types', {}).get('market_alert', False):
                    await self.send_notification(
                        user_id,
                        'market_alert',
                        market_data,
                        'low'
                    )
                    sent_count += 1

            logger.info(f"📊 Sent daily market insights to {sent_count} users")

        except Exception as e:
            logger.error(f"Daily market insights failed: {e}")

    async def _send_weekly_skill_recommendations(self):
        """Send weekly skill recommendations"""
        try:
            # Get trending skills
            trending_skills = await self._get_trending_skills()

            # Send personalized recommendations
            sent_count = 0
            for user_id in list(self.active_connections.keys()):
                # This would be personalized based on user profile
                await self.send_notification(
                    user_id,
                    'skill_recommendation',
                    {
                        'skill_name': trending_skills[0]['name'],
                        'reason': trending_skills[0]['reason'],
                        'trending_skills': trending_skills[:3]
                    },
                    'medium'
                )
                sent_count += 1

            logger.info(f"🎯 Sent weekly skill recommendations to {sent_count} users")

        except Exception as e:
            logger.error(f"Weekly skill recommendations failed: {e}")

    async def _get_market_insights(self) -> Dict[str, Any]:
        """Get current market insights"""
        try:
            from .trend_analyzer import trend_analyzer
            insights = trend_analyzer.analyze_skill_trends([], 1)  # Last month
            return {
                'skill': 'Python',
                'percentage': 15,
                'trend': 'growing',
                'top_skills': ['Python', 'AI/ML', 'Cloud Computing']
            }
        except:
            return {
                'skill': 'Python',
                'percentage': 12,
                'trend': 'growing'
            }

    async def _get_trending_skills(self) -> List[Dict]:
        """Get trending skills data"""
        return [
            {
                'name': 'Sustainable Finance',
                'reason': 'Green energy investments growing 25% YoY'
            },
            {
                'name': 'Carbon Accounting',
                'reason': 'New ESG reporting requirements'
            },
            {
                'name': 'Renewable Energy Tech',
                'reason': 'Solar and wind technology advancements'
            }
        ]

    async def cleanup_inactive_connections(self):
        """Clean up inactive WebSocket connections"""
        current_time = datetime.utcnow()
        inactive_threshold = timedelta(minutes=30)

        to_remove = []
        for websocket, metadata in self.connection_metadata.items():
            if current_time - metadata['last_activity'] > inactive_threshold:
                to_remove.append((websocket, metadata['user_id']))

        for websocket, user_id in to_remove:
            await self.disconnect(websocket)

        if to_remove:
            logger.info(f"🧹 Cleaned up {len(to_remove)} inactive connections")

    def get_connection_stats(self) -> Dict[str, Any]:
        """Get real-time connection statistics"""
        total_connections = sum(len(connections) for connections in self.active_connections.values())
        unique_users = len(self.active_connections)

        return {
            'total_connections': total_connections,
            'unique_users': unique_users,
            'active_users': unique_users,
            'connections_per_user_avg': total_connections / unique_users if unique_users > 0 else 0,
            'notification_queues_size': {user_id: queue.qsize() for user_id, queue in self.notification_queues.items() if not queue.empty()}
        }

# Global instance
realtime_notifications = AdvancedRealtimeNotifications()