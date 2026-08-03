from datetime import datetime
from sqlalchemy import Column, Integer, BigInteger, String, DateTime
from bot.sql_helper import Base, Session
from bot import LOGGER


class EmbyNameChangeHistory(Base):
    """Emby 用户名修改记录表"""
    __tablename__ = 'emby_name_change_history'

    id = Column(Integer, primary_key=True, autoincrement=True)
    tg = Column(BigInteger, nullable=False, comment="TG用户ID")
    tg_username = Column(String(255), nullable=True, comment="TG用户名/昵称")
    embyid = Column(String(255), nullable=True, comment="Emby用户ID")
    old_name = Column(String(255), nullable=True, comment="修改前用户名")
    new_name = Column(String(255), nullable=False, comment="修改后用户名")
    cost = Column(Integer, default=0, comment="消耗积分")
    created_at = Column(DateTime, default=datetime.now, comment="修改时间")


def sql_add_name_change_history(
    tg: int,
    tg_username: str,
    embyid: str,
    old_name: str,
    new_name: str,
    cost: int = 488
) -> bool:
    """
    添加一条用户名修改记录
    """
    try:
        with Session() as session:
            record = EmbyNameChangeHistory(
                tg=tg,
                tg_username=tg_username or '',
                embyid=embyid,
                old_name=old_name,
                new_name=new_name,
                cost=cost,
                created_at=datetime.now()
            )
            session.add(record)
            session.commit()
            LOGGER.info(f"新增改名记录: tg={tg}, {old_name} -> {new_name}")
            return True
    except Exception as e:
        LOGGER.error(f"添加改名记录失败: {e}")
        return False


def sql_get_name_change_history(limit: int = 50, offset: int = 0):
    """
    获取用户名修改记录，按时间倒序
    """
    try:
        with Session() as session:
            records = session.query(EmbyNameChangeHistory).order_by(
                EmbyNameChangeHistory.created_at.desc()
            ).limit(limit).offset(offset).all()
            return records
    except Exception as e:
        LOGGER.error(f"查询改名记录失败: {e}")
        return []


def sql_count_name_change_history() -> int:
    """
    获取改名记录总数
    """
    try:
        with Session() as session:
            return session.query(EmbyNameChangeHistory).count()
    except Exception as e:
        LOGGER.error(f"统计改名记录失败: {e}")
        return 0
