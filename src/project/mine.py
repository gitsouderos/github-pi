from project.config.db import get_session
from project.config.github_client import github_client
from sqlalchemy.orm import Session
from project.database_models.repositories import Repository as RepositoryModel
from project.database_models.organizations import Organization as OrganizationModel
from project.database_models.users import User as UserModel
from time import sleep


def insert_org(db: Session, org: OrganizationModel):
    try:
        db.add(org)
        db.commit()
        db.refresh(org)
    except Exception as e:
        print(f"[!] ERROR inserting Orangization:\n{e.__cause__}")
        db.rollback()
    return org


def insert_user(db: Session, user: UserModel):
    try:
        db.add(user)
        db.commit()
        db.refresh(user)
    except Exception as e:
        print(f"[!] ERROR inserting User:\n{e.__cause__}")
        db.rollback()
    return user


def insert_repo(db: Session, repo: RepositoryModel):
    try:
        db.add(repo)
        db.commit()
        db.refresh(repo)
    except Exception as e:
        print(f"[!] ERROR inserting Repo:\n{e}")
        db.rollback()
    return repo


def get_latest_insert_star_count(db: Session) -> int:

    latest_inserted: RepositoryModel = db.query(RepositoryModel).order_by(RepositoryModel.inserted_at.desc()).first()

    return latest_inserted.stargazers_count


def collect_data(db: Session):

    latest_star_count = get_latest_insert_star_count(db)
    while latest_star_count >= 1000:
        query = f"stars:1000..{latest_star_count} sort:stars-desc"
        repos = github_client.search_repositories(query)
        print(f"\n\n==>QUERY: {query}")
        print(f"TOTAL COUNT: {repos.totalCount}")
        idx = 0
        for repo in repos:
            rate_limit = github_client.get_rate_limit()
            if rate_limit.core.remaining < 10 or rate_limit.search.remaining < 10:
                sleep(60 * 10)
            idx += 1
            print(f"==>Fetched ({idx}/{repos.totalCount}): {repo}")
            print(f"[*] INFO: {rate_limit.search.remaining} searches left")
            print(f"[*] INFO: {rate_limit.core.remaining} requests left")
            repo_model = RepositoryModel.from_instance(repo)

            if repo.organization:
                org = OrganizationModel.from_instance(repo.organization)
                insert_org(db, org)
            if repo.parent:  # recursive loop of death??? probs not.. but maybe
                parent_repo_model = RepositoryModel.from_instance(repo.parent)
                insert_repo(db, parent_repo_model)
            if repo.owner:
                owner = UserModel.from_instance(repo.owner)
                insert_user(db, owner)

            insert_repo(db, repo_model)

        latest_star_count = get_latest_insert_star_count(db)
    return "Data collected"


if __name__ == "__main__":
    print("=>Started Mining")
    db_session = next(get_session())
    finished = collect_data(db_session)
    print(finished)
