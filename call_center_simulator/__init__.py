import random


class Lead:

    def __init__(self, lead_id, ltv, patience, talk_time):
        """
        Represents a lead.

        Parameters
        ----------
        lead_id : int
            Unique identifier.
        ltv : numeric
            Money lead spends if they convert.
        patience : numeric
            Amount of time (seconds) a lead will wait on hold before hanging
            up.
        talk_time : numeric
            Amount of time (seconds) the lead takes to talk to an agent before
            converting.
        """
        self.lead_id = lead_id
        self.patience = patience
        self.ltv = ltv
        self.talk_time = talk_time

    def __repr__(self):
        """
        String representation of a lead.
        """
        indent = '\t'*self.lead_id
        return '{}Lead{:02d}'.format(indent, self.lead_id)


def generate_lead(lead_id, min_patience, max_patience, min_ltv, max_ltv,
                  mean_talk_time):
    """Randomly initializes patience, ltv, and talk_time using provided
    distribution parameters.

    Parameters
    ----------
    lead_id : int
        Unique identifier.
    min_patience : numeric
        Min distribution parameter for patience (seconds).
    max_patience : numeric
        Max distribution parameter for patience (seconds).
    min_ltv : numeric
        Min distribution parameter for ltv (dollars).
    max_ltv : numeric
        Max distribution parameter for ltv (dollars).
    mean_talk_time : numeric
        Mean distribution parameter for talk_time (seconds).

    Returns
    -------
    Lead
        Instantiated lead.
    """
    patience = random.uniform(min_patience, max_patience)
    ltv = random.uniform(min_ltv, max_ltv)
    talk_time = random.expovariate(1.0 / mean_talk_time)
    lead = Lead(lead_id, ltv, patience, talk_time)
    return lead


def interval_lead_generator(env, agents, lead_scoring_model, results,
                            interval_dist_params, lead_dist_params):
    """
    Generator object which is responsible for calling the lead_generator at
    specified intervals.

    Parameters
    ----------
    env : simpy.Environment
        An Environment Implements a simulation environment which simulates
        the passing of time by stepping from event to event.
    agents : simpy.Resource
        A resource has a limited number of slots that can be requested by a
        process. If all slots are taken, requesters are put into a queue.
        If a process releases a slot, the next process is popped from the
        queue and gets oneslot.
    lead_scoring_model : LeadScoringModel
        A model for predicting the LTV of a lead. This is passed to the
        lead_generator and is used to prioritize the lead lead in the agent
        request queue.
    results : dict
        Book keeping object for storing results of events, e.g. which leads
        converted.
    interval_dist_params : dict
        Specifies the distribution parameters for interval and total number of
        leads generated. Keys are:
            * num_leads
            * lead_creation_interval
    lead_dist_params : dict
        Specifies the distribution parameters for lead generation. Keys are:
            * min_patience
            * max_patience
            * min_ltv
            * max_ltv
            * mean_talk_time

    Yields
    ------
    simpy.events.Timeout
        An Event that gets triggered after a specified delay.
    """
    num_leads = interval_dist_params['num_leads']
    interval = interval_dist_params['lead_creation_interval']
    for i in range(num_leads):
        c = lead_generator(env, i, agents, lead_scoring_model, results,
                           lead_dist_params)
        env.process(c)
        delay = random.expovariate(1.0 / interval)
        yield env.timeout(delay)


def lead_generator(env, lead_id, agents, lead_scoring_model, results,
                   lead_dist_params):
    """Lead generator.

    Responsible for
        * Creating lead
        * Handling lead requests to the agent resource. This includes
        specifying the priority of each request.
        * Book keeping of converted leads vs missed leads.

    A Lead is defined by their
        * name
        * patience
        * ltv
        * talk_time: time they'll spend talking to an agent

    Parameters
    ----------
    env : simpy.Environment
        An Environment Implements a simulation environment which simulates
        the passing of time by stepping from event to event.
    lead_id : int
        Unique ID of lead.
    agents : simpy.Resource
        A resource has a limited number of slots that can be requested by a
        process. If all slots are taken, requesters are put into a queue.
        If a process releases a slot, the next process is popped from the
        queue and gets oneslot.
    lead_scoring_model : LeadScoringModel
        A model for predicting the LTV of a lead. This is used to prioritize
        the lead lead in the agent request queue.
    results : dict
        Book keeping object for storing results of events, e.g. which leads
        converted.
    lead_dist_params : dict
        Specifies the distribution parameters for lead generation. Keys are:
            * min_patience
            * max_patience
            * min_ltv
            * max_ltv
            * mean_talk_time


    Yields
    ------
    1st yield
        simpy.events.Condition
            An <any> Condition event that gets triggered when either the agents
            request is processed or the patience timeout event is processed.
    2nd
        simpy.events.Timeout
            A Timeout event for with the time_on_phone as the delay.

    """
    arrive = env.now

    lead = generate_lead(lead_id, **lead_dist_params)

    print('%7.4f %s: Hesre I am' % (arrive, lead))

    lead_score = lead_scoring_model.predict(lead)
    with agents.request(priority=-1*lead_score) as req:
        # Wait for the agents or abort at the end of our tether
        # Yield
        #     req if agent is available
        #     lead patience timeout if agent isunavailable
        result = yield req | env.timeout(lead.patience)

        wait = env.now - arrive

        if req in result:
            # Lead got to the agent and converted
            print('%7.4f %s: Waited %6.3f' % (env.now, lead, wait))
            results['converted_leads'].append(lead)
            yield env.timeout(lead.talk_time)
            print('%7.4f %s: Converted' % (env.now, lead))

        else:
            # Lead hung up
            results['missed_leads'].append(lead)
            print('%7.4f %s: HUNG UP after %6.3f' % (env.now, lead, wait))


