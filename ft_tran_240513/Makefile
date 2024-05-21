DOCKER_COMPOSE = docker-compose --file ./docker-compose.yml

CYAN  := \033[1;36;40m
RESET := \033[0m
LOG   := printf "[$(CYAN)INFO$(RESET)] %s\n"

all:
	$(DOCKER_COMPOSE) up --build

clean:
	$(DOCKER_COMPOSE) down -v --rmi all --remove-orphans

fclean: clean
	@$(LOG) "fclean"
	@rm ./ft_back/ft_user/migrations/0001_initial.py
	@rm ./ft_back/ft_user/migrations/0002_alter_matchinfo_match_date.py
	@rm ./ft_back/ft_user/migrations/0003_gamestat_game_count_alter_matchinfo_match_date.py
	@rm ./ft_back/chatting/migrations/0001_initial.py
	docker system prune --volumes --all --force

re:
	make fclean
	make all

.PHONY: all up down clean fclean re
